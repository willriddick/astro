import pygame
from src.util import Vec2, swap_palette, Timer
from src.components import Entity, Collider, Sprite 
from src.particles import ParticleEmitter, BoostUpParticle
from src.camera import CAMERA
from src.clock import CLOCK
from src.sounds import SOUNDS
import src.graphics as graphics


class Rocket(Entity):

    PARTICLE_OFFSET = pygame.Vector2(8, 16)

    def __init__(self, position, size, palette_index=1):
        super().__init__(position, size)

        self.sprite = Sprite(position, image_offset=Vec2(0, 15))
        palette = graphics.PLAYER_PALETTES[palette_index]
        sheet = swap_palette(
            graphics.ROCKET,
            graphics.PLAYER_PALETTES[0],
            palette,
        )
        self.sprite.add_animation(0, [sheet], 0, (0, 1))
        
        self.particle_timer = Timer()
        self.particle_emitter = None

        self.speed = 50
        self.acceleration = 100

        self.collider = Collider(size)
        self.collider.add_owner(self)
        self.collider.update(position)
        self.collider.enabled = False

        self.enabled = False
        self.collected = False
        self.sprite.alpha = 100
    
    def update(self):
        self.particle_emitter.update()
        self.sprite.update(self.position)

        if self.collected:
            self.speed += self.acceleration * CLOCK.dt
            self.position.y -= (self.speed * CLOCK.dt)

            if self.particle_timer.is_done:
                CAMERA.screenshake(20, 3)
                self.particle_emitter.emit(
                    type=BoostUpParticle, 
                    position=self.position + self.PARTICLE_OFFSET,
                    count=5
                )
                self.particle_timer.start(100)
    
    def render(self, display, offset):
        super().render(display, offset)
        self.particle_emitter.render(display, offset)
    
    def enable(self):
        self.collider.enabled = True
        self.enabled = True
        self.sprite.alpha = 255
    
    def disable(self):
        self.collider.enabled = False
        self.enabled = False
        self.sprite.alpha = 100
    
    
    def spawn(self):
        self.particle_emitter = ParticleEmitter(30)
    
    def collect(self, _: Entity):
        self.collected = True
        self.collider.enabled = False
        SOUNDS.play('rocket')
        self.particle_timer.start(1)
    