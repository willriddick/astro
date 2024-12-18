from math import copysign
import pygame
from ..tilemap.tilemap import Tilemap
from ..tilemap.tilemap import Direction
from .util import load_image

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.rect_size = (7, 14)
        self.image = load_image('player.png')
        self.image_offset = (13, 18)

        self.move_speed: float = 2
        self.acc: float = 0.1
        self.dec: float = 0.2
        self.move_dir: int = 0
        self.velocity = pygame.math.Vector2(0, 0)

        self.jump_input = 0
        self.jump_buffer = 5
        self.coyote_timer = 0
        self.coyote_buffer = 5
        self.jump_speed = 4
        self.fall_speed = 3
        self.gravity = 0.1

        self.collisions = {
            Direction.UP: False,
            Direction.DOWN: False,
            Direction.RIGHT: False,
            Direction.LEFT: False
        }

        self.debug = True
        self.tiles_around = []

    def get_input(self):
        pressed = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        self.move_dir = int(pressed[pygame.K_d]) - int(pressed[pygame.K_a])

        self.jump_input = max(0, self.jump_input - 1)
        if just_pressed[pygame.K_SPACE]:
            self.jump_input = self.jump_buffer
    
    def get_rect(self):
        return pygame.FRect(self.pos.x, self.pos.y, self.rect_size[0], self.rect_size[1])
    
    def move(self, tilemap: Tilemap):
        # Update tile position
        tile_pos = (self.pos.x // tilemap.tile_size, self.pos.y // tilemap.tile_size)
        self.tiles_around = tilemap.get_tiles_around(tile_pos, ['stone'])

        # Reset collisions
        for k in self.collisions.keys():
            self.collisions[k] = False
        
        # Update y position
        self.pos.y += self.velocity.y
        entity_rect = self.get_rect()
        for tile in tilemap.get_tiles_around(tile_pos, ['stone']):
            rect = tile.get_rect()
            if entity_rect.colliderect(rect):
                if self.velocity.y > 0:
                    entity_rect.bottom = rect.top
                    self.collisions[Direction.DOWN] = True
                if self.velocity.y < 0:
                    entity_rect.top = rect.bottom
                    self.collisions[Direction.UP] = True
                self.pos.y = entity_rect.y
                self.velocity.y = 0
        
        # Update x position
        self.pos.x += self.velocity.x
        entity_rect = self.get_rect()
        for tile in tilemap.get_tiles_around(tile_pos, ['stone']):
            rect = tile.get_rect()
            if entity_rect.colliderect(rect):
                if self.velocity.x > 0:
                    entity_rect.right = rect.left
                    self.collisions[Direction.RIGHT] = True
                if self.velocity.x < 0:
                    entity_rect.left = rect.right
                    self.collisions[Direction.LEFT] = True
                self.pos.x = entity_rect.x
                self.velocity.x = 0
              
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
        
        self.move(tilemap)
        
    def render(self, display, offset=(0, 0)):
        display.blit(self.image, 
            (self.pos.x - self.image_offset[0] + offset[0], 
             self.pos.y - self.image_offset[1] + offset[1]))
        
        if self.debug:
            pygame.draw.rect(display, (255, 0, 0), self.get_rect().move(offset), 1)

            for tile in self.tiles_around:
                pygame.draw.rect(display, (0, 255, 0), tile.get_rect().move(offset), 1)
