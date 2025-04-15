import random
import math
import pygame
from src.util import swap_palette, Timer
from src.components import Entity, Collider, Sprite 
from src.particles import ParticleEmitter, FuelCellParticle
from src.camera import CAMERA
from src.sounds import SOUNDS
from src.clock import CLOCK
import src.graphics as graphics


class FuelCell(Entity):

    PARTICLE_OFFSET = pygame.Vector2(8, 8)

    def __init__(self, position, size, palette_index=1):
        super().__init__(position, size)
        self.spawn_position = position.copy()
        self.sprite = Sprite(position)
        palette = graphics.PLAYER_PALETTES[palette_index]
        sheet = swap_palette(
            graphics.FUEL_CELL,
            graphics.PLAYER_PALETTES[0],
            palette,
        )
        self.sprite.add_animation(0, [sheet], 0, (0, 1))
        
        self.particle_emitter = None
        self.particle_timer = Timer(100)

        self.collider = Collider(size)
        self.collider.add_owner(self)
        self.collider.update(position)

        self.x_bob_speed = random.randint(600, 1300)
        self.y_bob_speed = random.randint(600, 1300)
        self.x_bob_offset = random.randint(10, 25)
        self.y_bob_offset = random.randint(10, 25)

        self.collected = False
    
    def update(self):
        x_offset = self.x_bob_offset * math.sin(CLOCK.ticks * math.pi / self.x_bob_speed)
        self.position.x = self.spawn_position.x + x_offset
        y_offset = self.y_bob_offset * math.sin(CLOCK.ticks * math.pi / self.y_bob_speed)
        self.position.y = self.spawn_position.y + y_offset 

        self.particle_emitter.update()
        self.sprite.update(self.position)
        self.collider.update(self.position)

        if not self.collected and self.particle_timer.is_done:
            self.particle_emitter.emit(
                type=FuelCellParticle, 
                position=self.position + self.PARTICLE_OFFSET,
                count=1
            )
            self.particle_timer.start()
    
    def render(self, display, offset):
        self.particle_emitter.render(display, offset)
        super().render(display, offset)
    
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
  