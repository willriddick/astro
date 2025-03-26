from src.entities import Particle

class ParticleEmitter():
    def __init__(self):
        self.pool: list[Particle] = None

    def update(self):
        for p in self.pool:
            p.update()
    
    def render(self, display, offset):
        for p in self.pool:
            p.render(display, offset)
