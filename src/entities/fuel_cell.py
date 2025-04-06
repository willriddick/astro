import pygame
from src.util import swap_palette 
from src.components import Entity, Collider, Sprite 
from src.particles import ParticleEmitter, FuelCellParticle
from src.camera import CAMERA
from src.sounds import SOUNDS
import src.graphics as graphics


class FuelCell(Entity):

    PARTICLE_OFFSET = pygame.Vector2(8, 8)

    def __init__(self, position, size, palette_index=1):
        super().__init__(position, size)

        self.sprite = Sprite(position)
        palette = graphics.PLAYER_PALETTES[palette_index]
        sheet = swap_palette(
            graphics.FUEL_CELL,
            graphics.PLAYER_PALETTES[0],
            palette,
        )
        self.sprite.add_animation(0, [sheet], 0, (0, 1))
        
        self.particle_emitter = None

        self.collider = Collider(size)
        self.collider.add_owner(self)
        self.collider.update(position)

        self.collected = False
    
    def update(self):
        self.particle_emitter.update()
        self.sprite.update(self.position)
    
    def render(self, display, offset):
        super().render(display, offset)
        self.particle_emitter.render(display, offset)
    
    def spawn(self):
        self.particle_emitter = ParticleEmitter(10)
    
    def collect(self, _: Entity):
        self.collected = True
        self.collider.enabled = False
        self.sprite.alpha = 50
        CAMERA.screenshake(300, 5)
        SOUNDS.play('fuel_cell')
        self.particle_emitter.emit(
            type=FuelCellParticle, 
            position=self.position + self.PARTICLE_OFFSET,
            count=10
        )
  