import pygame
from src.tilemap import Tilemap
from src.util import Direction, StateMachine, approach, load_sprite_sheet, swap_palette, load_image, load_palette
from src.game.sprite import Sprite
from .states import States, Idle, Run, Air, Jump, WallSlide, WallJump
from .animation import Animation

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float]):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.rect_size = (7, 14)

        # Velocity and acceleration
        self.movement_multiplier = 1
        self.velocity = pygame.math.Vector2(0, 0)
        self.move_dir = 1 # starts at one because the player is facing right
        self.ground_move_speed: float = 1.15  
        self.ground_acc = (0.1, 0.2) # (acceleration, deceleration)
        self.air_move_speed: float = 1.15  
        self.air_acc = (0.05, 0.01)   

        # Gravity
        self.gravity_multiplier = 1
        self.gravity = 0.14
        self.fall_speed = 3

        # Jumping
        self.max_jumps = 1
        self.jumps_remaining = 0
        self.jump_speed = 3
        self.coyote_timer = 0
        self.coyote_buffer = 7
        self.variable_jump_multiplier = 0.7
        self.variable_jump_buffer = 15
        self.variable_jump_timer = 0

        # Wall jump and sliding
        self.wall_jump_duration = 12
        self.wall_jump_speed = (2.5, 2.7)
        self.wall_jump_acc = (0.13, 0.13)
        self.slide_speed = 0.5
        self.slide_gravity = 0.05
        self.slide_dir = 0
        self.slide_timer = 0
        self.slide_buffer = 10

        # Inputs
        self.holding_jump = False
        self.jump_input_timer = 0
        self.jump_input_buffer = 4
        self.pressed_left_timer = 0
        self.pressed_left_buffer = 5
        self.pressed_right_timer = 0
        self.pressed_right_buffer = 5

        # Collisions
        self.tiles_around = []
        self.falling = False
        self.on_ground = False
        self.collisions = { 
            Direction.UP: False,
            Direction.DOWN: False,
            Direction.RIGHT: False, 
            Direction.LEFT: False
        }

        # Setup sprite
        sheet = swap_palette(
            load_image('player/player.png', False),
            load_palette('player/palette.png'), 
            load_palette('player/palette3.png')
        )
        image_list = load_sprite_sheet(sheet, (32, 32))

        self.sprite = Sprite(pos, image_offset=(13, 18))
        self.sprite.add_animation(Animation.IDLE, image_list, 0, range_=(0,4))
        self.sprite.add_animation(Animation.RUN, image_list, 10, range_=(4,10))
        self.sprite.add_animation(Animation.AIR_UP, image_list, 0, range_=(10,11))
        self.sprite.add_animation(Animation.AIR_DOWN, image_list, 0, range_=(11,12))
        self.sprite.add_animation(Animation.FRONT, image_list, 0, range_=(12,13))
        self.sprite.add_animation(Animation.BACK, image_list, 0, range_=(13,14))
        self.sprite.set_animation(Animation.IDLE)

        self.rotate_timer = 0
        self.rotate_duration = 10
        self.rotate_choice = [1] # 0: back | 1: front 
        self.rotate_dir = 0
        self.last_move_dir = 1

        # Setup state machine
        self.state_machine = StateMachine(self, [
            Idle(),
            Run(),
            Jump(),
            Air(),
            WallSlide(),
            WallJump()
        ], debug=False)

    def update(self, tilemap):
        self.handle_input()
        self.state_machine.update()
        self.handle_collision(tilemap)
        self.sprite.update(self.pos)
    
    def apply_movement(self, dir_: int, max_speed: float, acc: tuple[float, float]):
        if dir_ == 0:
            self.velocity.x = approach(
                value=self.velocity.x,
                target=0,
                step=acc[1] * self.movement_multiplier
            )
        else:
            self.velocity.x = approach(
                value=self.velocity.x,
                target=dir_ * max_speed * self.movement_multiplier,
                step=acc[0] * self.movement_multiplier
            )
    
    def apply_gravity(self, gravity: float, max_speed: float, ):
        self.velocity.y = min(
            max_speed * self.gravity_multiplier,
            self.velocity.y + gravity * self.gravity_multiplier
        )
    
    def handle_jump(self):
        self.coyote_timer = max(0, self.coyote_timer - 1)

        if self.on_ground:
            self.coyote_timer = self.coyote_buffer
            self.jumps_remaining = self.max_jumps
        
       
        if self.jump_input_timer > 0 and self.jumps_remaining:
            self.state_machine.switch(States.JUMP)
   
    def handle_wall_jump(self):
        self.slide_timer = max(0, self.slide_timer - 1)

        if self.collisions[Direction.RIGHT] and self.pressed_right_timer:
            self.slide_timer = self.slide_buffer
            self.slide_dir = 1
        elif self.collisions[Direction.LEFT] and self.pressed_left_timer:
            self.slide_timer = self.slide_buffer
            self.slide_dir = -1
        
        if self.jump_input_timer > 0 and self.slide_timer:
            self.state_machine.switch(States.WALL_JUMP)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        self.move_dir = int(pressed[pygame.K_d]) - int(pressed[pygame.K_a])
        
        self.jump_input_timer = max(0, self.jump_input_timer - 1)
        if just_pressed[pygame.K_SPACE]:
            self.jump_input_timer = self.jump_input_buffer
        
        self.holding_jump = pressed[pygame.K_SPACE]

        if pressed[pygame.K_a]:
            self.pressed_left_timer = self.pressed_left_buffer
        if pressed[pygame.K_d]:
            self.pressed_right_timer = self.pressed_right_buffer
        
        self.pressed_left_timer = max(0, self.pressed_left_timer - 1)
        self.pressed_right_timer = max(0, self.pressed_right_timer - 1)
    
    def set_animation(self, animation: Animation):
        self.sprite.set_animation(animation)
    
    def get_rect(self):
        return pygame.FRect(self.pos.x, self.pos.y, self.rect_size[0], self.rect_size[1])
       
    def handle_collision(self, tilemap: Tilemap):
        # Update tile position
        tile_pos = (self.pos.x // tilemap.tile_size, self.pos.y // tilemap.tile_size)
        self.tiles_around = tilemap.get_tiles_around(tile_pos, ['stone'])

        # Update y position
        self.pos.y += self.velocity.y
        entity_rect = self.get_rect()
        for tile in self.tiles_around:
            rect = tile.get_rect()
            if entity_rect.colliderect(rect):
                if self.velocity.y > 0:
                    entity_rect.bottom = rect.top
                if self.velocity.y < 0:
                    entity_rect.top = rect.bottom
                self.pos.y = entity_rect.y
                self.velocity.y = 0

        # Update x position
        self.pos.x += self.velocity.x
        entity_rect = self.get_rect()
        for tile in self.tiles_around:
            rect = tile.get_rect()
            if entity_rect.colliderect(rect):
                if self.velocity.x > 0:
                    entity_rect.right = rect.left
                if self.velocity.x < 0:
                    entity_rect.left = rect.right
                self.pos.x = entity_rect.x
                self.velocity.x = 0
        
        # Update collisions
        points = {
            Direction.DOWN:  [(entity_rect.left + 1,  entity_rect.bottom + 1),
                              (entity_rect.right - 1, entity_rect.bottom + 1)],
            Direction.UP:    [(entity_rect.left + 1,  entity_rect.top - 1),
                              (entity_rect.right - 1, entity_rect.top - 1)],
            Direction.LEFT:  [(entity_rect.left - 1,  entity_rect.top + 1),
                              (entity_rect.left - 1,  entity_rect.bottom - 1)],
            Direction.RIGHT: [(entity_rect.right + 1, entity_rect.top + 1),
                              (entity_rect.right + 1, entity_rect.bottom - 1)],
        }
        for direction, points in points.items():
            for tile in self.tiles_around:
                tile_rect = tile.get_rect()
                if any(tile_rect.collidepoint(point) for point in points):
                    self.collisions[direction] = True
                    break # No need to check further tiles for this direction
                else:
                    self.collisions[direction] = False
        
        # Update helper variables
        self.on_ground = self.collisions[Direction.DOWN]
        self.falling = (self.velocity.y > 0 and not self.collisions[Direction.DOWN])

    def render(self, display, offset=(0, 0)):
        self.sprite.render(display, offset)
        