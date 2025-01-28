import pygame
from src.util import State
from src.game.gravity import Gravity
from ..player import Player
from ..enums import Animations, States

class Air(State):
    def __init__(self):
        super().__init__(States.AIR)
    
    def on_enter(self):
        self.owner.sprite.set_next(Animations.AIR_UP if self.owner.velocity.y < 0 else Animations.AIR_DOWN)

    def update(self):
        nearest = self.owner.collider.get_nearest(Gravity)
        if nearest:
            self.owner.gravity_multiplier = nearest.gravity_multiplier
            self.owner.velocity_multiplier = pygame.Vector2(0.75, 0.75)
        else:
            self.owner.gravity_multiplier = 1
            self.owner.velocity_multiplier = pygame.Vector2(1, 1)

        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.handle_jump()
        self.owner.handle_wall_jump()
        self.owner.accelerate_x(self.owner.move_dir.x, Player.AIR_MOVE_SPEED, Player.AIR_ACC)

        # handle rotation animation
        if self.owner.rotated:
            self.owner.sprite.set_animation_duration(Animations.FRONT, Player.AIR_ROTATE_DURATION)
        self.owner.sprite.set_next(Animations.AIR_UP if self.owner.velocity.y < 0 else Animations.AIR_DOWN)
        
        if self.owner.move_dir.x != 0:
            self.owner.sprite.flip = self.owner.move_dir.x == -1

        # switch states
        if self.owner.wall_slide_timer.is_active:
            self.switch(States.WALL_SLIDE)

        if self.owner.on_ground:
            if self.owner.velocity.y == Player.FALL_SPEED:
                self.owner.camera.screenshake(15, 1)

            if self.owner.velocity.x == 0:
                self.switch(States.IDLE)
            else:
                self.switch(States.RUN)
 