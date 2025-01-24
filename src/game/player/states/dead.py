import pygame
from src.util import State, Direction
from ..player import Player
from ..enums import Animations, States

class Dead(State):
    def __init__(self):
        super().__init__(States.DEAD)
        self.timer = 0
    
    def on_enter(self):
        self.timer = 60
        self.owner.sprite.set_animation(Animations.IDLE_A)
        self.owner.apply_force(2, Direction.UP)
        self.owner.health_component.disable()
    
    def update(self):
        self.timer = max(0, self.timer - 1)

        self.owner.accelerate_x(1, 0, Player.AIR_ACC)
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)

        if self.timer == 0:
            self.owner.spawn(self.owner.level.spawn_pos)
