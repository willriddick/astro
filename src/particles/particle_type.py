class ParticleType:
    """Defines the properties of a particle, allowing flexible behavior changes."""
    def __init__(self, 
        size: tuple[int, int] = (2, 2), 
        size_growth: float = 0,
        duration: int = 300, 
        color=(255, 255, 255),
        x_velocity: tuple[float, float] = (-1, 1), y_velocity: tuple[float, float] = (-1, 1),
        gravity: int = 0
    ):
        self.size = size
        self.size_growth = size_growth
        self.duration = duration
        self.color = color
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.gravity = gravity


BoostUpParticle = ParticleType(
    size=(3, 5), 
    size_growth=-0.75,
    duration=700, 
    color=(255, 255, 255), 
    x_velocity=(-0.3, 0.3), 
    y_velocity=(0.5, 1),
    gravity=50
)

BoostDownParticle = ParticleType(
    size=(3, 5), 
    size_growth=-0.75,
    duration=700, 
    color=(255, 255, 255), 
    x_velocity=(-0.3, 0.3), 
    y_velocity=(-0.2, -0.7),
    gravity=50
)

LandParticle = ParticleType(
    size=(2, 4),
    size_growth=-0.3,
    duration=700, 
    color=(42, 47, 78), 
    x_velocity=(-0.6, 0.6), 
    y_velocity=(-0.2, -0.4), 
    gravity=120
)

StepParticle = ParticleType(
    size=(2, 2),
    size_growth=0,
    duration=500, 
    color=(66, 76, 110), 
    x_velocity=(-0.5, 0.5), 
    y_velocity=(-0.2, -0.4), 
    gravity=100
)

HurtParticle = ParticleType(
    size=(2, 3),
    size_growth=0.2,
    duration=1000, 
    color=(137, 30, 45), 
    x_velocity=(-0.4, 0.4), 
    y_velocity=(0, -0.8), 
    gravity=150
)

WallSlideLeftParticle = ParticleType(
    size=(2, 3),
    size_growth=0,
    duration=400,
    color=(66, 76, 110), 
    x_velocity=(0.1, 0.3),
    y_velocity=(-0.2, -0.3),
    gravity=50
)

WallSlideRightParticle = ParticleType(
    size=(2, 3),
    size_growth=0,
    duration=400,
    color=(66, 76, 110), 
    x_velocity=(-0.1, -0.3),
    y_velocity=(-0.2, -0.3),
    gravity=50
)

ShootingStarParticle = ParticleType(
    size=(2, 3),
    size_growth=-0.5,
    duration=1000,
    color=(255, 255, 255), 
    x_velocity=(-3, 3),
    y_velocity=(-3, 3)
)

FuelCellParticle = ParticleType(
    size=(4, 6),
    size_growth=-0.5,
    duration=1000, 
    color=(245, 160, 151), 
    x_velocity=(-0.3, 0.3), 
    y_velocity=(-0.3, 0.3)
)
