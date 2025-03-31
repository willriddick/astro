import random
import pygame
from src.util import State, Timer
from src.sounds import SOUNDS
from src.particles import StepParticle
from ..player import Player
from ..enums import Animations, States


class Run(State):
    def __init__(self):
        super().__init__(States.RUN)

    def on_enter(self):
        self.owner.sprite.set_next(Animations.RUN)
        if self.owner.rotated:
            self.owner.sprite.set_animation_duration(Animations.FRONT, Player.ROTATE_DURATION, Animations.RUN)
        
    def update(self):
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.accelerate_x(self.owner.input_dir.x, Player.GROUND_MOVE_SPEED, Player.GROUND_ACC)
        self.owner.handle_jump()
        self.owner.handle_boost()

        # play step sound
        frame = self.owner.sprite.frame
        if (frame == 2 or frame == 5) and self.owner.sprite.frame_changed:
            SOUNDS.play('step')
            self.owner.particle_emitter.emit(StepParticle, self.owner.position + pygame.Vector2(4, 14))

        # animate player
        if self.owner.rotated:
            self.owner.sprite.set_animation_duration(Animations.FRONT, Player.ROTATE_DURATION, Animations.RUN)
        
        if self.owner.input_dir.x != 0:
            self.owner.sprite.flip_x = self.owner.input_dir.x == -1

        # switch states
        if self.owner.velocity.x == 0:
            self.switch(States.IDLE)
        
        if not self.owner.on_ground:
            self.switch(States.AIR)
        