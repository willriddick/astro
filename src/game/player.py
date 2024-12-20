from math import copysign 
from random import choice
import pygame
from ..tilemap import Tilemap
from ..util import Direction, Sprite, load_sprite_sheet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int]):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.rect_size = (7, 14)

        self.sprite = Sprite(
            self.pos, 
            (13, 18)
        )
        self.sprite.add_animation('idle', load_sprite_sheet('player/idle.png', (32, 32)), 0)
        self.sprite.add_animation('run', load_sprite_sheet('player/run.png', (32, 32)), 10)
        self.sprite.add_animation('air_up', load_sprite_sheet('player/air_up.png', (32, 32)), 0)
        self.sprite.add_animation('air_down', load_sprite_sheet('player/air_down.png', (32, 32)), 0)
        self.sprite.add_animation('front', load_sprite_sheet('player/front.png', (32, 32)), 0)
        self.sprite.add_animation('back', load_sprite_sheet('player/back.png', (32, 32)), 0)
        self.sprite.set_animation('idle')

        self.rotate_timer = 0
        self.rotate_duration = 8
        self.rotate_choice = [1] # 0: back | 1: front 
        self.rotate_dir = 0

        self.move_speed: float = 1.2
        self.ground_acc = (0.1, 0.2)
        self.air_acc = (0.05, 0.01)
        self.move_dir = 1 # starts at one because the player is facing right
        self.last_move_dir = 1
        self.velocity = pygame.math.Vector2(0, 0)

        self.gravity = 0.13
        self.fall_speed = 3

        self.holding_jump = False
        self.jump_speed = 3
        self.variable_jump_multiplier = 0.7
        self.variable_jump_buffer = 30
        self.variable_jump_timer = 0
        self.jump_input = 0
        self.jump_buffer = 4
        self.coyote_timer = 0
        self.coyote_buffer = 5

        self.on_ground = False
        self.collisions = { 
            Direction.UP: False,
            Direction.DOWN: False,
            Direction.RIGHT: False, 
            Direction.LEFT: False
        }

        self.debug = False
        self.tiles_around = []
    
    def update(self, tilemap):
        self.get_input()

        # Update x velocity
        acc = self.ground_acc if self.on_ground else self.air_acc
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
        if self.on_ground:
            self.coyote_timer = self.coyote_buffer
        
        # Apply jump
        if self.jump_input > 0 and self.coyote_timer > 0:
            self.velocity.y = -self.jump_speed
            self.jump_input = 0
            self.coyote_timer = 0
            self.variable_jump_timer = self.variable_jump_buffer
        
        # Handle variable jump height
        self.variable_jump_timer = max(0, self.variable_jump_timer - 1)
        if not self.holding_jump and self.variable_jump_timer > 0 and self.velocity.y < 0:
            self.velocity.y *= self.variable_jump_multiplier
        
        # Move player with collisions
        self.move(tilemap)
        self.handle_animation(self.pos)

    def handle_animation(self, pos: pygame.math.Vector2):
        # Update rotate timer
        self.rotate_timer = max(0, self.rotate_timer - 1)

        # Detect direction change
        if self.move_dir != 0 and self.move_dir != self.last_move_dir:
            self.rotate_timer = self.rotate_duration
            self.rotate_dir = choice(self.rotate_choice)

        # Update the last move direction
        if self.move_dir != 0:
            self.last_move_dir = self.move_dir

        if self.on_ground:
            if self.rotate_timer > 0:
                if self.rotate_dir:
                    self.sprite.set_animation('front')
                else:
                    self.sprite.set_animation('back')
            elif self.move_dir != 0:
                self.sprite.set_animation('run')
            else:
                self.sprite.set_animation('idle')
        else:
            if self.rotate_timer > 0:
                if self.rotate_dir:
                    self.sprite.set_animation('front')
                else:
                    self.sprite.set_animation('back')
            elif self.velocity.y < 0:
                self.sprite.set_animation('air_up')
            else:
                self.sprite.set_animation('air_down')

        self.sprite.update(pos)
    
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
        
        self.on_ground = self.collisions[Direction.DOWN]

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
        
        self.holding_jump = pressed[pygame.K_SPACE]

    def render(self, display, offset=(0, 0)):
        self.sprite.render(display, offset)
        
        if self.debug:
            pygame.draw.rect(display, (255, 0, 0), self.get_rect().move(offset), 1)

            for tile in self.tiles_around:
                pygame.draw.rect(display, (0, 255, 0), tile.get_rect().move(offset), 1)
