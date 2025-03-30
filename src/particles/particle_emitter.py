import pygame
from .particle import Particle
from .particle_type import ParticleType


class ParticleEmitter():
    def __init__(self,  pool_size: int):
        self.pool: list[Particle] = [Particle() for _ in range(pool_size)]
    
    def update(self):
        for p in self.pool:
            if p.active:
                p.update()
    
    def render(self, display, offset):
        for p in self.pool:
            if p.active:
                p.render(display, offset)
    
    def emit(self, type: ParticleType, position: pygame.Vector2, count: int=1):
        """Attempt to spawn the given number of particles at the given position."""
        emitted = 0
        for particle in self.pool:
            if emitted >= count:
                break
            if not particle.active:
                particle.spawn(type, position)
                emitted += 1
