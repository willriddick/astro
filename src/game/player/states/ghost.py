import pygame
from src.util import State
from .player_state import PlayerState
from ..animation import Animation

class Ghost(State):
    def __init__(self):
        super().__init__(PlayerState.GHOST)
    
    def on_enter(self):
        self.owner.velocity = pygame.Vector2(0, 0)
        self.owner.set_animation(Animation.RUN)
        self.owner.collision_enabled = False
    
    def on_exit(self):
        self.owner.collision_enabled = True

    def update(self):
        self.owner.accelerate_x(self.owner.move_dir.x, self.owner.air_move_speed, self.owner.air_acc * 2) 
        self.owner.accelerate_y(self.owner.move_dir.y, self.owner.air_move_speed, self.owner.air_acc * 2) 

        if self.owner.move_dir.x != 0:
            self.owner.sprite.flip = self.owner.move_dir.x == -1
