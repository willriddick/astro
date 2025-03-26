from src.util import Vec2


class ParticleType:
    """Defines the properties of a particle, allowing flexible behavior changes."""
    def __init__(self, 
        size: Vec2, duration: int = 500, color=(255, 255, 255),
        x_velocity: tuple[float, float] = (-1, 1), y_velocity: tuple[float, float] = (-1, 1)
    ):
        self.size = size
        self.duration = duration
        self.color = color
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity


BoostUpParticle = ParticleType(Vec2(2, 2), 500, (255, 255, 255), (-0.5, 0,5), (0.5, 1.5))
