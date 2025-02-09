import pygame
from src.util import Assets, Direction, StateMachine, load_sprite_sheet, swap_palette, Vec2, Timer
from src.game.components import PhysicsEntity, Collider, HealthComponent, Sprite 
from src.game.exit import Exit
from .enums import Animations, States

class Player(PhysicsEntity):
    GROUND_MOVE_SPEED = 80
    GROUND_ACC = (360, 720) # (acceleration, deceleration)
    AIR_MOVE_SPEED = 90
    AIR_ACC = (180, 36)
    PRESSED_LEFT_BUFFER = 120
    PRESSED_RIGHT_BUFFER = 120

    GRAVITY = 485
    FALL_SPEED = 180

    DROP_SPEED = 30

    JUMP_INPUT_BUFFER = 50
    JUMP_SPEED = 185
    MAX_JUMPS = 1
    COYOTE_BUFFER = 115 # time after falling to allow jump
    VARIABLE_JUMP_MULTIPLIER = 0.93 # multiplies velocity when releasing jump
    VARIABLE_JUMP_BUFFER = 300 # time after jumping to allow variable jump

    SLIDE_DURATION = 200 # after this time, the player will decelerate to 0
    INITIAL_SLIDE_MULTIPLIER = 1.3 # multiplies velocity when entering slide state
    SLIDE_SPEED = 110
    SLIDE_ACC = (180, 180)

    WALL_JUMP_DURATION = 10 # time after wall jumping before switching to AIR
    WALL_JUMP_SPEED = Vec2(110, 160)
    WALL_JUMP_ACC = (150, 8)
    WALL_SLIDE_SPEED = 30
    WALL_SLIDE_GRAVITY = 180
    WALL_SLIDE_BUFFER = 150 # amount of time after wall sliding to allow wall jump

    ROTATE_DURATION = 180 # time to play FRONT animation when rotating
    AIR_ROTATE_DURATION = 250

    def __init__(self, palette_index: int=1):
        super().__init__(pygame.Vector2(0, 0), size=Vec2(8, 13))

        self.camera = None
        self.input_dir = pygame.Vector2(1, 0) # starts at one because the player is facing right
        self.slide_dir = 0
        self.spawn_position = pygame.Vector2(0, 0)

        self.just_boosted_timer = Timer(1000)

        # jumping and wall sliding
        self.jumps_remaining = 0
        self.coyote_timer = Timer(Player.COYOTE_BUFFER)
        self.variable_jump_timer = Timer(Player.VARIABLE_JUMP_BUFFER)
        self.wall_slide_dir = 0
        self.wall_slide_timer = Timer(Player.WALL_SLIDE_BUFFER)
        self.consecutive_wall_jumps = 0

        # inputs
        self.holding_jump = False
        self.just_pressed_down = False
        self.jump_input_timer = Timer(Player.JUMP_INPUT_BUFFER)
        self.pressed_left_timer = Timer(Player.PRESSED_LEFT_BUFFER)
        self.pressed_right_timer = Timer(Player.PRESSED_RIGHT_BUFFER)

        # setup sprite
        self.palette_index = palette_index
        self.rotated = False
        self.facing_dir = 0
        self.last_facing_dir = 1
        self.load_sprite(palette_index)
    
        # setup collider
        self.collider = Collider(size=Vec2(6, 13), offset=Vec2(1, 0))
        self.collider.add_owner(self)

        self.health_component = HealthComponent(self.collider, 3, 1000)
        self.health_component.on_damaged = self.on_damage
        self.health_component.on_death = self.on_death

        # setup state machine
        from .states import (Idle, Run, Air, Jump, WallSlide, WallJump, 
            Ghost, Slide, Hurt, Dead, Spawn, Drop, BoostUp)
        self.state_machine = StateMachine(self, [
            Idle(), Run(), Jump(), Air(), Slide(), WallSlide(), 
            WallJump(), Ghost(), Hurt(), Dead(), Spawn(), Drop(), BoostUp(),
        ])

    @property
    def debug(self) -> str:
        return (
            f'x:{int(self.position.x):4} y:{int(self.position.y):4}\n'
            f'hp: {self.health_component.health}\n'
            f'state: {self.state_machine.current_state.name}\n'
            f'vel:{self.velocity.x:4.0f} {self.velocity.y:4.0f}\n'
            f'cols: {' '.join(dir_.name[0] for dir_, val in self.collisions.items() if val)}\n'
        )
    
    def update(self):
        self.handle_input()
        self.sprite.update(self.position)
        self.health_component.update(self.position)
        self.state_machine.update()
        self.handle_collision()

        if self.collider.get_nearest(Exit):
            print('EXIT')
        
    def set_position(self, position: pygame.Vector2):
        self.position = position
        self.health_component.update(position)
        self.sprite.set_pos(position)

    def spawn(self, position: pygame.Vector2):
        self.spawn_position = position
        self.set_state(States.SPAWN)
    
    def on_damage(self):
        self.set_state(States.HURT)
    
    def on_death(self):
        self.set_state(States.DEAD)
    
    def apply_damage(self, damage: int):
        self.health_component.apply_damage(damage)
    
    def set_state(self, state: 'States'):
        self.state_machine.switch(state)

    def get_state(self) -> 'States':
        return self.state_machine.current_state.id
    
    def toggle_ghost(self):
        if self.get_state() == States.GHOST:
            self.set_state(States.AIR)
        else:
            self.set_state(States.GHOST)
    
    def handle_jump(self):
        if self.on_ground:
            self.coyote_timer.start()
            self.jumps_remaining = Player.MAX_JUMPS
       
        if self.jump_input_timer.is_active and self.jumps_remaining:
            self.state_machine.switch(States.JUMP)
       
        if not self.holding_jump and self.variable_jump_timer.is_active and self.velocity.y < 0:
            self.velocity.y *= Player.VARIABLE_JUMP_MULTIPLIER
   
    def handle_wall_jump(self):
        if self.on_ground:
            self.consecutive_wall_jumps = 0
        else:
            if self.collisions[Direction.RIGHT] and self.pressed_right_timer.is_active:
                self.wall_slide_timer.start()
                self.wall_slide_dir = 1
            elif self.collisions[Direction.LEFT] and self.pressed_left_timer.is_active:
                self.wall_slide_timer.start()
                self.wall_slide_dir = -1
        
        if (not self.collisions[Direction.LEFT] and not self.collisions[Direction.RIGHT]):
            self.wall_slide_timer.reset()
        
        if self.jump_input_timer.is_active and self.wall_slide_timer.is_active:
            self.state_machine.switch(States.WALL_JUMP)
    
    def handle_collision(self) -> None:
        # if pressing down, drop through platform
        self.platform_collision = (self.input_dir.y == 1 and self.state_machine.current_state.id != States.SLIDE)

        # handle collision
        super().handle_collision()

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        just_pressed = pygame.key.get_just_pressed()

        # update input direction
        self.input_dir = pygame.Vector2(
            int(pressed[pygame.K_d]) - int(pressed[pygame.K_a]),
            int(pressed[pygame.K_s]) - int(pressed[pygame.K_w])
        )

        self.just_pressed_down = just_pressed[pygame.K_s]

        # update rotated field
        if self.input_dir.x != 0 and self.input_dir.x != self.last_facing_dir:
            self.rotated = True
        else:
            self.rotated = False
        
        if self.input_dir.x != 0:
            self.last_facing_dir = self.input_dir.x
 
        # update jumping input timer
        self.holding_jump = pressed[pygame.K_SPACE]
        if just_pressed[pygame.K_SPACE]:
            self.jump_input_timer.start()

        # update pressed left/right input timer
        if pressed[pygame.K_a]:
            self.pressed_left_timer.start()
        if pressed[pygame.K_d]:
            self.pressed_right_timer.start()
    
    def load_sprite(self, palette_index: int):
        self.palette_index = palette_index % len(Assets.PLAYER_PALETTES)

        sheet = swap_palette(
            Assets.PLAYER_SHEET,
            Assets.PLAYER_PALETTES[0],
            Assets.PLAYER_PALETTES[self.palette_index],
        )
        image_list = load_sprite_sheet(sheet, (16, 18))
        
        self.sprite = Sprite(self.position, image_offset=Vec2(4, 5))
        self.sprite.add_animation(Animations.IDLE_A, image_list, 0, range_=(0,1))
        self.sprite.add_animation(Animations.IDLE_B, image_list, 5, range_=(0,4))
        self.sprite.add_animation(Animations.RUN, image_list, 12, range_=(4,10))
        self.sprite.add_animation(Animations.AIR_UP, image_list, 0, range_=(10,11))
        self.sprite.add_animation(Animations.AIR_DOWN, image_list, 0, range_=(11,12))
        self.sprite.add_animation(Animations.FRONT, image_list, 0, range_=(12,13))
        self.sprite.add_animation(Animations.BACK, image_list, 0, range_=(13,14))
        self.sprite.add_animation(Animations.WALL_SLIDE, image_list, 0, range_=(14,15))
        self.sprite.add_animation(Animations.SLIDE, image_list, 0, range_=(15,16))
        self.sprite.add_animation(Animations.DROP, image_list, 0, range_=(16,17))
