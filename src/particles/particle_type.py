from src.util import Vec2


class ParticleType:
    """Defines the properties of a particle, allowing flexible behavior changes."""
    def __init__(self, 
        size: Vec2 = Vec2(2, 2), duration: int = 300, color=(255, 255, 255),
        x_velocity: tuple[float, float] = (-1, 1), y_velocity: tuple[float, float] = (-1, 1),
        gravity: int = 0
    ):
        self.size = size
        self.duration = duration
        self.color = color
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.gravity = gravity

BoostUpParticle = ParticleType(
    size=Vec2(2, 2), 
    duration=700, 
    color=(255, 255, 255), 
    x_velocity=(-0.3, 0.3), 
    y_velocity=(0.5, 1),
    gravity=50
)

BoostDownParticle = ParticleType(
    size=Vec2(2, 2), 
    duration=700, 
    color=(255, 255, 255), 
    x_velocity=(-0.3, 0.3), 
    y_velocity=(-0.2, -0.7),
    gravity=50
)

LandParticle = ParticleType(
    size=Vec2(2, 2),
    duration=500, 
    color=(66, 76, 110), 
    x_velocity=(-0.5, 0.5), 
    y_velocity=(-0.2, -0.3), 
    gravity=100
)

HurtParticle = ParticleType(
    size=Vec2(2, 2),
    duration=400, 
    color=(137, 30, 45), 
    x_velocity=(-0.3, 0.3), 
    y_velocity=(0, -0.6), 
    gravity=100
)

