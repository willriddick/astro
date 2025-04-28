import pygame
from src.util import Direction, StateMachine, Vec2, Timer, approach
from src.components import PhysicsEntity, Collider, HealthComponent
from src.entities import Rocket, FuelCell
from src.particles import ParticleEmitter
from src.clock import CLOCK
from src.debug import DEBUG
from src.settings import SETTINGS
from src.inputs import INPUTS
from src.sounds import SOUNDS
from src.level_manager import LEVEL_MANAGER
from .enums import States


class Player(PhysicsEntity):
    GROUND_MOVE_SPEED = 80
    GROUND_ACC = (360, 720) # (acceleration, deceleration)
    AIR_MOVE_SPEED = 90
    AIR_ACC = (180, 36)
    PRESSED_LEFT_BUFFER = 120
    PRESSED_RIGHT_BUFFER = 120

    GRAVITY = 485
    FALL_SPEED = 180

    INDICATOR_OFFSET = 70

    FUEL_UI_COLOR_INDEX = 13
    FUEL_UI_OFFSET = pygame.Vector2(-2, -8)
    MAX_FUEL = 100
    REFUEL_TIME = 500  # duration in milliseconds after boosting to start refueling
    REFUEL_RATE = 50  # rate of refueling (fuel per second)

    BOOST_ACC = 100

    BOOST_UP_COST = 5  # minimum fuel required to boost up and display UI
    INITIAL_BOOST_UP = 5
    BOOST_UP_SPEED = 50
    BOOST_UP_MOVE_SPEED = 60
    BOOST_UP_MOVE_ACC = Vec2(100, 20)

    BOOST_DOWN_COST = 15
    INITIAL_BOOST_DOWN = 40
    BOOST_DOWN_SPEED = 200
    BOOST_DOWN_MOVE_SPEED = 75
    BOOST_DOWN_MOVE_ACC = Vec2(180, 20)

    JUMP_INPUT_BUFFER = 50
    JUMP_SPEED = 185
    MAX_JUMPS = 1
    COYOTE_BUFFER = 115  # time after falling to allow jump
    VARIABLE_JUMP_MULTIPLIER = 0.93  # multiplies velocity when releasing jump
    VARIABLE_JUMP_BUFFER = 300  # time after jumping to allow variable jump

    SLIDE_DURATION = 200  # after this time, the player will decelerate to 0
    INITIAL_SLIDE_SPEED = 85  # minimum speed when entering slide state
    INITIAL_SLIDE_MULTIPLIER = 1.5  # multiplies velocity when entering slide state
    SLIDE_SPEED = 120
    SLIDE_ACC = (180, 180)

    WALL_JUMP_DURATION = 10  # time after wall jumping before switching to AIR
    WALL_JUMP_SPEED = Vec2(110, 160)
    WALL_JUMP_ACC = (150, 8)
    WALL_SLIDE_SPEED = 30
    WALL_SLIDE_GRAVITY = 180
    WALL_SLIDE_BUFFER = 150  # amount of time after wall sliding to allow wall jump

    ROTATE_DURATION = 180  # time to play FRONT animation when rotating
    AIR_ROTATE_DURATION = 250

    def __init__(self, palette_index: int=1, multiplayer: bool=False):
        super().__init__(pygame.Vector2(0, 0), size=Vec2(8, 13))

        self.visible = True

        self.paused = False
        self.paused_timer = Timer()
        self.multiplayer = multiplayer

        # tracks jetpack particles for multiplayer 
        self.current_particle = 0

        self.input_dir = Vec2(0, 0)
        self.spawn_position = pygame.Vector2(0, 0)
        self.slide_dir = 0

        self.fuel_ui_color = None
        self.fuel = Player.MAX_FUEL 
        self.refuel_timer = Timer(Player.REFUEL_TIME)

        self.particle_emitter = ParticleEmitter(50)

        # jumping and wall sliding
        self.jumps_remaining = 0
        self.coyote_timer = Timer(Player.COYOTE_BUFFER)
        self.variable_jump_timer = Timer(Player.VARIABLE_JUMP_BUFFER)
        self.wall_slide_dir = 0
        self.wall_slide_timer = Timer(Player.WALL_SLIDE_BUFFER)
        self.consecutive_wall_jumps = 0

        # inputs
        self.holding_jump = False
        self.pressed_down = False
        self.jump_input_timer = Timer(Player.JUMP_INPUT_BUFFER)
        self.pressed_left_timer = Timer(Player.PRESSED_LEFT_BUFFER)
        self.pressed_right_timer = Timer(Player.PRESSED_RIGHT_BUFFER)

        # setup sprite
        self.rotated = False
        self.last_facing_dir = 1
        self.palette_index = palette_index
        self.sprite = None
        self.load_sprite(palette_index)
    
        # setup collider
        self.collider = Collider(size=Vec2(6, 13), offset=Vec2(1, 0))
        self.collider.add_owner(self)

        self.health_component = HealthComponent(self.collider, 3, 1000)
        self.health_component.on_damaged = self.on_damage
        self.health_component.on_death = self.on_death

        # setup state machine
        from .states import (
            Idle, Run, Air, Jump, WallSlide, WallJump, 
            Ghost, Slide, Hurt, Dead, Spawn, BoostUp, BoostDown
        )
        self.state_machine = StateMachine(self, [
            Idle(), Run(), Jump(), Air(), Slide(), WallSlide(), 
            WallJump(), Ghost(), Hurt(), Dead(), Spawn(), BoostUp(),
            BoostDown(), 
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
    
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        if self.visible:
            self.particle_emitter.render(display, offset)
            self.draw_fuel_bar(display, offset)
            #self.draw_indicator(display, offset)
            super().render(display, offset)
    
    def update(self):
        if DEBUG.enabled:
            DEBUG.add_display(self.debug)

        if not self.paused:
            self.handle_input()
        
        if self.paused_timer.duration != -1:
            self.paused = self.paused_timer.is_active

        if not self.paused or self.multiplayer:
            self.sprite.update(self.position)
            self.health_component.update(self.position)
            self.state_machine.update()
            self.particle_emitter.update()
            self.handle_collision()
            self.handle_collectables()
            self.handle_fuel()
    
    def pause(self, duration: int):
        """
        Pause the player for a given duration.

        duration: use -1 to pause indefinitely
        """
        if duration == -1:
            self.paused_timer.duration = duration
        else:
            self.paused_timer.start(duration)

        self.paused = True
        self.input_dir = Vec2(0, 0)
        self.holding_jump = False
        self.pressed_down = False
    
    def unpause(self):
        self.paused_timer.reset()
        self.paused = False
        
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
    
    def handle_collectables(self):
        rocket = self.collider.get_nearest(Rocket)
        if rocket:
            rocket.collect(self)
        
        fuel_cell = self.collider.get_nearest(FuelCell)
        if fuel_cell:
            fuel_cell.collect(self)
    
    def handle_fuel(self):
        if (
            self.state_machine.current_state.id != States.BOOST_UP
            and self.state_machine.current_state.id != States.BOOST_DOWN
            and self.refuel_timer.is_done 
            and self.fuel != Player.MAX_FUEL
        ):
            self.fuel = approach(self.fuel, Player.MAX_FUEL, Player.REFUEL_RATE * CLOCK.dt)
    
    def handle_boost(self):
        if self.input_dir.y == -1:
            if self.fuel >= Player.BOOST_UP_COST:
                self.set_state(States.BOOST_UP)
        
        if self.fuel < Player.BOOST_UP_COST and INPUTS.get('up', just_pressed=True):
            SOUNDS.play('cant_boost')

        if self.pressed_down:
            if self.fuel > Player.BOOST_DOWN_COST:
                self.set_state(States.BOOST_DOWN)
            else:
                SOUNDS.play('cant_boost')

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
            # if player is holding down, wall jump down by redirecting to BOOST_DOWN state
            if self.input_dir.y == 1:
                self.velocity.x = Player.WALL_JUMP_SPEED.x * -self.wall_slide_dir * self.velocity_multiplier.x 
                self.velocity.y = -80  # upper velocity to reduce speed of downward boost
                self.state_machine.switch(States.BOOST_DOWN)
            else:
                # other wise, send to wall jump state
                self.state_machine.switch(States.WALL_JUMP)
    
    def handle_collision(self) -> None:
        # if pressing down, drop through platform
        self.platform_collision = (self.input_dir.y == 1 and self.state_machine.current_state.id != States.SLIDE)

        # handle collision
        super().handle_collision()

    def handle_input(self):
        self.input_dir = INPUTS.get_dir()

        # update rotated field
        if self.input_dir.x != 0 and self.input_dir.x != self.last_facing_dir:
            self.rotated = True
        else:
            self.rotated = False
        
        if self.input_dir.x != 0:
            self.last_facing_dir = self.input_dir.x
 
        # update jumping input timer
        self.holding_jump = INPUTS.get('jump')
        if INPUTS.get('jump', just_pressed=True):
            self.jump_input_timer.start()
        
        # boost down
        self.pressed_down = INPUTS.get('down', just_pressed=True)

        # update pressed left/right input timer
        if self.input_dir.x == -1:
            self.pressed_left_timer.start()
        if self.input_dir.x == 1:
            self.pressed_right_timer.start()
    
    def load_sprite(self, palette_index: int):
        from .sprite import load_sprite
        self.palette_index = palette_index
        self.sprite, self.fuel_ui_color = load_sprite(palette_index)

    def draw_indicator(self, display: pygame.Surface, offset: pygame.Vector2):
        exit_pos = LEVEL_MANAGER.current.exit_pos
        if exit_pos and exit_pos.distance_to(self.center) > (Player.INDICATOR_OFFSET * 2):
            indicator_pos = self.center + (exit_pos - self.position).normalize() * Player.INDICATOR_OFFSET 
            pygame.draw.circle(display, (255, 255, 255), indicator_pos + offset, 3)
            
    def draw_fuel_bar(self, display: pygame.Surface, offset: pygame.Vector2):
        """Draw a fuel bar expanding symmetrically from the center."""
        if (
            self.fuel < Player.BOOST_UP_COST 
            or self.fuel == Player.MAX_FUEL
            or self.get_state() == States.DEAD
        ):
            return
        
        bar_width = 10
        fuel_percentage = max(self.fuel / Player.MAX_FUEL, 0)
        fuel_fill_width = int(bar_width * fuel_percentage)
        fuel_pos = offset + self.position + Player.FUEL_UI_OFFSET

        # oosition the fuel fill at the bottom and expand symmetrically
        surface = pygame.Surface((bar_width, 1), pygame.SRCALPHA)
        alpha = 255 * (SETTINGS.get('fuel_ui_alpha') / 10)
        surface.set_alpha(alpha)

        center_x = bar_width // 2
        left_x = center_x - (fuel_fill_width // 2)
        right_x = center_x + (fuel_fill_width // 2)

        pygame.draw.line(surface, self.fuel_ui_color, (left_x, 0), (right_x, 0))
        display.blit(surface, fuel_pos)
