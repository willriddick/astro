import pygame
from src.util import State, Timer
from src.sounds import SOUNDS
from ..enums import States
from ..player import Player

class Spawn(State):
    def __init__(self):
        super().__init__(States.SPAWN)
        self.timer = Timer(20)

    def on_enter(self):
        self.owner.collision_enabled = True
        self.owner.velocity = pygame.Vector2(0, 0)
        self.owner.set_position(self.owner.spawn_position + pygame.Vector2(0, 4))
        self.owner.health_component.reset()
        self.owner.visible = True
        self.owner.sprite.reset()
        self.owner.fuel = Player.MAX_FUEL
        self.timer.start()
        SOUNDS.play('spawn')
    
    def update(self):
        if self.timer.is_done:
            self.switch(States.IDLE)