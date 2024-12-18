from math import copysign
import pygame
from ..tilemap.tilemap import Tilemap
from ..tilemap.tilemap import Direction
from .util import load_image

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.image = load_image('player.png')
        self.image_offset = (13, 18)
        self.rect_size = (7, 14)
        self.rect = pygame.FRect(0, 0, self.rect_size[0], self.rect_size[1])
        self.rect.centerx, self.rect.bottom = pos

        self.jump_input = 0
        self.jump_buffer = 5

        self.coyote_timer = 0
        self.coyote_buffer = 5

        self.jump_speed = 4
        self.fall_speed = 3
        self.gravity = 0.1

        self.move_speed: float = 2
        self.acc: float = 0.1
        self.dec: float = 0.2
        self.move_dir: int = 0
        self.velocity = pygame.math.Vector2(0, 0)

        self.collisions = {
            Direction.UP: False,
            Direction.DOWN: False,
            Direction.RIGHT: False,
            Direction.LEFT: False
        }

    def get_input(self):
        pressed = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        self.move_dir = int(pressed[pygame.K_d]) - int(pressed[pygame.K_a])

        self.jump_input = max(0, self.jump_input - 1)
        if just_pressed[pygame.K_SPACE]:
            self.jump_input = self.jump_buffer


    def handle_collisions(self, tilemap: Tilemap):
        # Reset collisions
        for k in self.collisions.keys():
            self.collisions[k] = False
        
        # Calculate frame movement
        frame_movement = pygame.math.Vector2(self.velocity.x, self.velocity.y)
        tile_pos = (self.rect.x // tilemap.tile_size, self.rect.y // tilemap.tile_size)
        
        # Update x position
        self.rect.x += frame_movement.x
        for rect in tilemap.get_rects_around(tile_pos, ['stone']):
            if self.rect.colliderect(rect):
                if frame_movement.x > 0:
                    self.rect.right = rect.left
                    self.collisions[Direction.RIGHT] = True
                if frame_movement.x < 0:
                    self.rect.left = rect.right
                    self.collisions[Direction.LEFT] = True
                self.velocity.x = 0
        
        # Update y position
        self.rect.y += frame_movement.y
        for rect in tilemap.get_rects_around(tile_pos, ['stone']):
            if self.rect.colliderect(rect):
                if frame_movement.y > 0:
                    self.rect.bottom = rect.top
                    self.collisions[Direction.DOWN] = True
                if frame_movement.y < 0:
                    self.rect.top = rect.bottom
                    self.collisions[Direction.UP] = True
                self.velocity.y = 0
        
    def update(self, tilemap):
        self.get_input()

        if self.move_dir == 0:
            # Apply deceleration
            if abs(self.velocity.x) < self.dec:
                self.velocity.x = 0
            else:
                # Copysign returns the first argument with the sign of the second argument
                self.velocity.x -= copysign(self.dec, self.velocity.x)
        else:
            # Apply acceleration, clamping velocity to the move speed
            self.velocity.x = max(
                -self.move_speed, 
                min(self.move_speed, self.velocity.x + (self.move_dir * self.acc)))
        
        # Apply gravity
        if not self.collisions[Direction.DOWN]:
            self.velocity.y = min(self.fall_speed, self.velocity.y + self.gravity)

        # Update coyote timer
        self.coyote_timer = max(0, self.coyote_timer - 1)
        if self.collisions[Direction.DOWN]:
            self.coyote_timer = self.coyote_buffer
        
        # Apply jump
        if self.jump_input > 0 and self.coyote_timer > 0:
            self.velocity.y = -self.jump_speed
            self.jump_input = 0
            self.coyote_timer = 0
        
        self.handle_collisions(tilemap)
        
    def render(self, display, offset=(0, 0)):
        display.blit(self.image, 
            (self.rect.x - self.image_offset[0] + offset[0], 
             self.rect.y - self.image_offset[1] + offset[1]))
        pygame.draw.rect(display, (255, 0, 0), self.rect.move(offset), 1)
