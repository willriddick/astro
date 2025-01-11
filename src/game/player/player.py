import pygame
from src.util import Direction, StateMachine, load_sprite_sheet, swap_palette, load_image, load_palette
from src.game.sprite import Sprite
from src.game.physics_entity import PhysicsEntity
from .player_state import PlayerState
from .animation import Animation

class Player(PhysicsEntity):
    GROUND_MOVE_SPEED = 1.15
    GROUND_ACC = (0.1, 0.2)
    AIR_MOVE_SPEED = 1.3
    AIR_ACC = (0.05, 0.01)

    GRAVITY = 0.14
    FALL_SPEED = 3

    JUMP_SPEED = 3
    MAX_JUMPS = 1
    COYOTE_BUFFER = 7
    VARIABLE_JUMP_MULTIPLIER = 0.8
    VARIABLE_JUMP_BUFFER = 10

    SLIDE_INPUT_BUFFER = 14
    SLIDE_DURATION = 15
    INITIAL_SLIDE_MULTIPLIER = 1.3
    SLIDE_SPEED = 1.6
    SLIDE_ACC = (0.05, 0.05)

    WALL_JUMP_DURATION = 10
    WALL_JUMP_SPEED = (2, 2.5)
    WALL_JUMP_ACC = (0.13, 0.13)
    WALL_SLIDE_SPEED = 0.5
    WALL_SLIDE_GRAVITY = 0.05
    WALL_SLIDE_BUFFER = 10

    JUMP_INPUT_BUFFER = 4
    PRESSED_LEFT_BUFFER = 5
    PRESSED_RIGHT_BUFFER = 5

    ROTATE_DURATION = 11
    ROTATE_CHOICE = [1] # 0: back | 1: front 

    def __init__(self, pos: tuple[float, float]=pygame.Vector2(0, 0)):
        super().__init__(pos, (8, 14))

        # Velocity and acceleration
        self.move_dir = pygame.Vector2(1, 0) # starts at one because the player is facing right

        # Jumping
        self.jumps_remaining = 0
        self.coyote_timer = 0
        self.variable_jump_timer = 0

        # Sliding
        self.slide_input_timer = 0
        self.slide_dir = 0

        # Wall jump and sliding
        self.wall_slide_dir = 0
        self.wall_slide_timer = 0

        # Inputs
        self.holding_jump = False
        self.jump_input_timer = 0
        self.pressed_left_timer = 0
        self.pressed_right_timer = 0

        # Setup sprite
        sheet = swap_palette(
            load_image('player/player.png', False),
            load_palette('player/palette_key.png'), 
            load_palette('player/palette2.png')
        )
        image_list = load_sprite_sheet(sheet, (16, 18))

        self.sprite = Sprite(pos, image_offset=(4, 4))
        self.sprite.add_animation(Animation.IDLE, image_list, 5, range_=(0,4))
        self.sprite.add_animation(Animation.RUN, image_list, 10, range_=(4,10))
        self.sprite.add_animation(Animation.AIR_UP, image_list, 0, range_=(10,11))
        self.sprite.add_animation(Animation.AIR_DOWN, image_list, 0, range_=(11,12))
        self.sprite.add_animation(Animation.FRONT, image_list, 0, range_=(12,13))
        self.sprite.add_animation(Animation.BACK, image_list, 0, range_=(13,14))
        self.sprite.add_animation(Animation.WALL_SLIDE, image_list, 0, range_=(14,15))
        self.sprite.add_animation(Animation.SLIDE, image_list, 0, range_=(15,16))
        self.sprite.set_animation(Animation.IDLE)

        self.rotate_timer = 0
        self.rotate_dir = 0
        self.last_rotate_dir = 1

        # Setup state machine
        from .states import Idle, Run, Air, Jump, WallSlide, WallJump, Ghost, Slide
        self.state_machine = StateMachine(self, [
            Idle(),
            Run(),
            Jump(),
            Air(),
            Slide(),
            WallSlide(),
            WallJump(),
            Ghost()
        ])

    def update(self, tilemap):
        self.handle_input()
        self.state_machine.update()
        self.handle_collision(tilemap)
        self.sprite.update(self.pos)
    
    def set_state(self, state: PlayerState):
        self.state_machine.switch(state)

    def get_state(self) -> PlayerState:
        return self.state_machine.current_state.id
    
    def handle_jump(self):
        self.coyote_timer = max(0, self.coyote_timer - 1)

        if self.on_ground:
            self.coyote_timer = Player.COYOTE_BUFFER
            self.jumps_remaining = Player.MAX_JUMPS
       
        if self.jump_input_timer > 0 and self.jumps_remaining:
            self.state_machine.switch(PlayerState.JUMP)
        
        self.variable_jump_timer = max(0, self.variable_jump_timer - 1)
        if not self.holding_jump and self.variable_jump_timer > 0 and self.velocity.y < 0:
            self.velocity.y *= (Player.VARIABLE_JUMP_MULTIPLIER / (1 / self.gravity_multiplier))
   
    def handle_wall_jump(self):
        self.wall_slide_timer = max(0, self.wall_slide_timer - 1)

        if self.collisions[Direction.RIGHT] and self.pressed_right_timer:
            self.wall_slide_timer = Player.WALL_SLIDE_BUFFER
            self.wall_slide_dir = 1
        elif self.collisions[Direction.LEFT] and self.pressed_left_timer:
            self.wall_slide_timer = Player.WALL_SLIDE_BUFFER
            self.wall_slide_dir = -1
        
        if (not self.collisions[Direction.LEFT] and not self.collisions[Direction.RIGHT]):
            self.wall_slide_timer = 0
        
        if self.jump_input_timer > 0 and self.wall_slide_timer:
            self.state_machine.switch(PlayerState.WALL_JUMP)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        self.move_dir = pygame.Vector2(
            int(pressed[pygame.K_d]) - int(pressed[pygame.K_a]),
            int(pressed[pygame.K_s]) - int(pressed[pygame.K_w])
        )
        
        self.holding_jump = pressed[pygame.K_SPACE]
        self.jump_input_timer = max(0, self.jump_input_timer - 1)
        if just_pressed[pygame.K_SPACE]:
            self.jump_input_timer = Player.JUMP_INPUT_BUFFER

        self.slide_input_timer = max(0, self.slide_input_timer - 1)
        if just_pressed[pygame.K_s]:
            self.slide_input_timer = Player.SLIDE_INPUT_BUFFER

        self.pressed_left_timer = max(0, self.pressed_left_timer - 1)
        if pressed[pygame.K_a]:
            self.pressed_left_timer = Player.PRESSED_LEFT_BUFFER

        self.pressed_right_timer = max(0, self.pressed_right_timer - 1)
        if pressed[pygame.K_d]:
            self.pressed_right_timer = Player.PRESSED_RIGHT_BUFFER
        