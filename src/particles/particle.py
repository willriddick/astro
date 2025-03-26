import random
import pygame
from src.components import Entity
from src.util import Vec2, Timer, draw_circle
from src.clock import CLOCK
from .particle_type import ParticleType


class Particle(Entity):
    def __init__(self):
        super().__init__((0, 0), (0, 0))
        self.type = None
        self.active = False
        self.alpha = 255
        self.timer = Timer()

    def update(self):
        if not self.active:
            return
        
        self.position += self.velocity * CLOCK.dt
        self.alpha = 255 * (1 - self.timer.progress)
        
        if self.timer.is_done:
            self.despawn()

    def render(self, display, offset):
        draw_circle(
            display, offset, 
            self.position, 
            self.type.size.x, 
            (*self.type.color, self.alpha),
        )

    def spawn(self, type: ParticleType, position: pygame.Vector2):
        """Spawn the particle at the given position."""
        self.type = type
        self.active = True
        self.timer.start(type.duration)

        self.position = position.copy()
        self.velocity = Vec2(
            random.uniform(type.x_velocity[0], type.x_velocity[1]) * 100, 
            random.uniform(type.y_velocity[0], type.y_velocity[1]) * 100
        )

    def despawn(self):
        self.active = False
    