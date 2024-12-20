from math import copysign
import pygame
from ..tilemap.tilemap import Tilemap
from ..tilemap.tilemap import Direction
from .util import load_image, load_sprite_sheet
from .sprite import Sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.rect_size = (7, 14)

        self.sprite = Sprite(
            self.pos, 
            (13, 18)
        )
        self.sprite.add_animation('idle', load_sprite_sheet('player/idle.png', (32, 32)),0)
        self.sprite.add_animation('run', load_sprite_sheet('player/run.png', (32, 32)), 12)
        self.sprite.add_animation('air', load_sprite_sheet('player/air.png', (32, 32)),0)
        self.sprite.set_animation('idle')

        self.move_speed: float = 1.5
        self.ground_acc = (0.2, 0.3)
        self.air_acc = (0.1, 0.05)
        self.move_dir: int = 0
        self.velocity = pygame.math.Vector2(0, 0)

        self.jump_speed = 3
        self.fall_speed = 3
        self.gravity = 0.14
        self.grounded = False

        self.jump_input = 0
        self.jump_buffer = 4
        self.coyote_timer = 0
        self.coyote_buffer = 5

        self.collisions = {
            Direction.UP: False,
            Direction.DOWN: False,
            Direction.RIGHT: False,
            Direction.LEFT: False
        }

        self.debug = False
        self.tiles_around = []
    
    def get_rect(self):
        return pygame.FRect(self.pos.x, self.pos.y, self.rect_size[0], self.rect_size[1])

    def get_input(self):
        pressed = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        self.move_dir = int(pressed[pygame.K_d]) - int(pressed[pygame.K_a])
        if self.move_dir != 0:
            self.sprite.flip = self.move_dir == -1

        self.jump_input = max(0, self.jump_input - 1)
        if just_pressed[pygame.K_SPACE]:
            self.jump_input = self.jump_buffer
    
    def update(self, tilemap):
        self.get_input()

        # Update x velocity
        acc = self.ground_acc if self.grounded else self.air_acc
        if self.move_dir == 0:
            # Apply deceleration
            if abs(self.velocity.x) < acc[1]:
                self.velocity.x = 0
            else:
                # Copysign returns the first argument with the sign of the second argument
                self.velocity.x -= copysign(acc[1], self.velocity.x)
        else:
            # Apply acceleration, clamping velocity to the move speed
            self.velocity.x = max(
                -self.move_speed, 
                min(self.move_speed, self.velocity.x + (self.move_dir * acc[0])))
        
        # Apply gravity
        self.velocity.y = min(self.fall_speed, self.velocity.y + self.gravity)
        
        # Update coyote timer
        self.coyote_timer = max(0, self.coyote_timer - 1)
        if self.grounded:
            self.coyote_timer = self.coyote_buffer
        
        # Apply jump
        if self.jump_input > 0 and self.coyote_timer > 0:
            self.velocity.y = -self.jump_speed
            self.jump_input = 0
            self.coyote_timer = 0
        
        # Move player with collisions
        self.move(tilemap)

        # Update sprite
        if self.grounded:
            if self.move_dir != 0:
                self.sprite.set_animation('run')
            else:
                self.sprite.set_animation('idle')
        else:
            self.sprite.set_animation('air')

        self.sprite.update(self.pos)
    
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
                    self.grounded = True
                if self.velocity.y < 0:
                    entity_rect.top = rect.bottom
                    self.collisions[Direction.UP] = True
                self.pos.y = entity_rect.y
                self.velocity.y = 0
        
        if self.velocity.y != 0 and not self.collisions[Direction.DOWN]:
            self.grounded = False

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
        
    def render(self, display, offset=(0, 0)):
        self.sprite.render(display, offset)
        
        if self.debug:
            pygame.draw.rect(display, (255, 0, 0), self.get_rect().move(offset), 1)

            for tile in self.tiles_around:
                pygame.draw.rect(display, (0, 255, 0), tile.get_rect().move(offset), 1)
