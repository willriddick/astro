import pygame
from src.util import State, Timer
from ..enums import States

class Spawn(State):
    def __init__(self):
        super().__init__(States.SPAWN)
        self.timer = Timer(20)

    def on_enter(self):
        self.owner.velocity = pygame.Vector2(0, 0)
        self.owner.set_position(self.owner.spawn_position + pygame.Vector2(0, 4))
        self.owner.health_component.reset()
        self.timer.start()
    
    def update(self):
        if self.timer.is_done:
            self.switch(States.IDLE)