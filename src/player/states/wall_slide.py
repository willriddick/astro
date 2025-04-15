import pygame
from src.util import State, Direction, Timer
from src.sounds import SOUNDS
from src.particles import WallSlideLeftParticle, WallSlideRightParticle
from ..player import Player
from ..enums import Animations, States


class WallSlide(State):
    def __init__(self):
        super().__init__(States.WALL_SLIDE)
        self.timer = Timer(200)

    def on_enter(self):
        self.owner.sprite.flip_x = (self.owner.wall_slide_dir == 1)
        self.owner.sprite.set_animation(Animations.WALL_SLIDE)
        SOUNDS.play('wall')
    
    def on_exit(self):
        self.owner.last_rotate_dir = -self.owner.wall_slide_dir
        self.owner.pressed_left_timer.reset()
        self.owner.pressed_right_timer.reset()
    
    def update(self):
        if self.owner.velocity.y < 0 or self.owner.input_dir.x != self.owner.wall_slide_dir:
            # apply normal gravity if not wall sliding
            self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        else:
            # apply wall slide gravity and animation
            self.owner.apply_gravity(Player.WALL_SLIDE_GRAVITY, Player.WALL_SLIDE_SPEED)
            self.owner.sprite.set_animation(Animations.WALL_SLIDE)

            # emit particles every 200ms
            if self.timer.is_done:
                if self.owner.wall_slide_dir == -1:
                    offset = pygame.Vector2(0, 3)
                    particle = WallSlideLeftParticle 
                else:
                    offset = pygame.Vector2(8, 3)
                    particle = WallSlideRightParticle

                self.owner.particle_emitter.emit(
                    type=particle,
                    position=self.owner.position + offset,
                    count=1
                )
                self.timer.start()
        
        # use AIR animation if not wall sliding
        if self.owner.input_dir.x != self.owner.wall_slide_dir:
            self.owner.sprite.set_animation(Animations.AIR_DOWN if self.owner.falling else Animations.AIR_UP)
        
        # update velocity
        self.owner.accelerate_x(self.owner.input_dir.x, Player.AIR_MOVE_SPEED, Player.AIR_ACC)
        self.owner.handle_wall_jump()

        # switch to IDLE or RUN state
        if self.owner.on_ground:
            self.switch(States.IDLE if self.owner.velocity.x == 0 else States.RUN)
            SOUNDS.play('land')
        
        # switch to AIR state 
        if (
            (self.owner.wall_slide_dir == -1 and not self.owner.collisions[Direction.LEFT])
            or (self.owner.wall_slide_dir == 1 and not self.owner.collisions[Direction.RIGHT])
        ):
            self.switch(States.AIR)
        