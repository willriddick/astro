import pygame
from src.util import State
from ..player import Player, PlayerState, Animation

class Ghost(State):
    def __init__(self):
        super().__init__(PlayerState.GHOST)
    
    def on_enter(self):
        self.owner.velocity = pygame.Vector2(0, 0)
        self.owner.sprite.set_animation(Animation.RUN)
        self.owner.collision_enabled = False
    
    def on_exit(self):
        self.owner.collision_enabled = True

    def update(self):
        self.owner.accelerate_x(self.owner.move_dir.x, Player.AIR_MOVE_SPEED, Player.AIR_ACC * 2) 
        self.owner.accelerate_y(self.owner.move_dir.y, Player.AIR_MOVE_SPEED, Player.AIR_ACC * 2)

        if self.owner.move_dir.x != 0:
            self.owner.sprite.flip = self.owner.move_dir.x == -1
