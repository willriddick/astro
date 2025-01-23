import pygame
from src.util import State
from ..player import Player
from ..enums import Animations, States

class Ghost(State):
    def __init__(self):
        super().__init__(States.GHOST)
    
    def on_enter(self):
        self.owner.velocity = pygame.Vector2(0, 0)
        self.owner.sprite.set_animation(Animations.RUN)
        self.owner.collision_enabled = False
    
    def on_exit(self):
        self.owner.collision_enabled = True

    def update(self):
        multiplier = 3 if self.owner.holding_jump else 1
            
        self.owner.accelerate_x(self.owner.move_dir.x, Player.AIR_MOVE_SPEED * multiplier, Player.GROUND_ACC * 3 * multiplier) 
        self.owner.accelerate_y(self.owner.move_dir.y, Player.AIR_MOVE_SPEED * multiplier, Player.GROUND_ACC * 3 * multiplier)

        if self.owner.move_dir.x != 0:
            self.owner.sprite.flip = self.owner.move_dir.x == -1
