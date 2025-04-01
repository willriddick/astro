import pygame
from src.util import Vec2, swap_palette, Timer
from src.components import Entity, Collider, Sprite 
from src.particles import ParticleEmitter, BoostUpParticle
from src.camera import CAMERA
from src.clock import CLOCK
from src.sounds import SOUNDS
from src.level_manager import LEVEL_MANAGER
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

        self.next_timer = Timer()

        self.collider = Collider(size)
        self.collider.add_owner(self)
        self.collider.update(position)

        self.collected = False
    
    def update(self):
        self.particle_emitter.update()
        self.sprite.update(self.position)

        if self.collected:
            CAMERA.screenshake(10, 1)
            self.position.y -= (50 * CLOCK.dt)

            if self.particle_timer.is_done:
                self.particle_emitter.emit(
                    type=BoostUpParticle, 
                    position=self.position + self.PARTICLE_OFFSET,
                    count=5
                )
                self.particle_timer.start(100)
            
            if self.next_timer.is_done:
                LEVEL_MANAGER.new_level(config_index=1)
    
    def render(self, display, offset):
        super().render(display, offset)
        self.particle_emitter.render(display, offset)
    
    def spawn(self):
        self.particle_emitter = ParticleEmitter(30)
    
    def collect(self, player: Entity):
        self.collected = True
        self.collider.enabled = False
        self.particle_timer.start(1)

        player.visible = False
        player.pause(2500)
        SOUNDS.play('rocket')
        CAMERA.transition(3000, 0)
        self.next_timer.start(1500)
  