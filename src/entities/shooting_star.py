import random
import pygame
from src.util import Timer
from src.level_manager import LEVEL_MANAGER
from src.particles import ParticleEmitter, ShootingStarParticle


SHOOTING_STAR_DURATION = 3000
VARIATION = 2000


class ShootingStar():
    def __init__(self):
        self.particle_emitter = ParticleEmitter(1)
        self.timer = Timer(SHOOTING_STAR_DURATION)
        self.timer.start(SHOOTING_STAR_DURATION + random.randint(-VARIATION, VARIATION))
        self.width = LEVEL_MANAGER.current.tilemap.rect.width
        self.height = LEVEL_MANAGER.current.tilemap.rect.height
    
    def update(self):
        self.particle_emitter.update()

        if self.timer.is_done:
            position = pygame.Vector2(
                random.randint(0, self.width),
                random.randint(0, self.height)
            ) 
            self.particle_emitter.emit(ShootingStarParticle, position)
            self.timer.start(SHOOTING_STAR_DURATION + random.randint(-VARIATION, VARIATION))
    
    def render(self, display, offset):
        self.particle_emitter.render(display, offset)
    