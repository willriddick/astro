import pygame
from src.util import State, Direction, Timer
from ..player import Player
from ..enums import Animations, States

class Dead(State):
    def __init__(self):
        super().__init__(States.DEAD)
        self.timer = Timer(1000)
    
    def on_enter(self):
        self.timer.start()
        self.owner.sprite.reset()
        self.owner.sprite.flash(self.timer.duration, pygame.Color(255, 0, 0), pygame.BLEND_RGB_MULT)
        self.owner.sprite.set_animation(Animations.IDLE_A)
        self.owner.apply_force(2, Direction.UP)
        self.owner.health_component.disable()
    
    def update(self):
        self.owner.accelerate_x(1, 0, Player.AIR_ACC)
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)

        if self.timer.is_done:
            self.owner.spawn(self.owner.level.spawn_pos)
