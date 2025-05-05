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

        self.current_size = 0
        self.size = 0
        self.size_growth = 1
        self.position = pygame.Vector2(0, 0)

    def update(self):
        if not self.active:
            return
        
        self.position += self.velocity * CLOCK.dt
        self.alpha = 255 * (1 - self.timer.progress)

        # calculate current size:
        # for a positive growth factor, the particle increases in size
        # for a negative value, it decreases
        self.current_size = self.size * (1 + self.size_growth * self.timer.progress)

        if self.type.gravity:
            self.velocity = pygame.Vector2(
                self.velocity.x,
                self.velocity.y + self.type.gravity * CLOCK.dt
            )
        
        if self.timer.is_done:
            self.despawn()

    def render(self, display, offset, override_alpha=255):
        color = (*self.type.color, min(self.alpha, override_alpha))
        draw_circle(
            display, offset, 
            center=self.position, 
            radius=self.current_size,
            fill_color=color,
        )

    def spawn(self, type: ParticleType, position: pygame.Vector2):
        """Spawn the particle at the given position."""
        self.type = type
        self.active = True
        self.timer.start(type.duration)

        self.position = position.copy()

        if type.size[0] == type.size[1]:
            self.size = type.size[0]
        else:
            self.size = random.randint(type.size[0], type.size[1])

        self.size_growth = type.size_growth

        self.velocity = Vec2(
            random.uniform(type.x_velocity[0], type.x_velocity[1]) * 100, 
            random.uniform(type.y_velocity[0], type.y_velocity[1]) * 100
        )

    def despawn(self):
        self.active = False
    