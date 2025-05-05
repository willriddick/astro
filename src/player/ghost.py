import pygame
from src.util import Vec2, Timer
from src.components import Entity
from src.settings import SETTINGS
from src.particles import ParticleEmitter, BoostUpParticle, BoostDownParticle, StepParticle
import src.graphics as graphics
from .enums import Animations
from .sprite import load_sprite


BOOST_OFFSET = 9


class Ghost(Entity):

    TAG_OFFSET = Vec2(4, -16)
    TAG_ALPHA = 100

    def __init__(self, username: str, palette_index=2):
        super().__init__(pygame.Vector2(0, 0), Vec2(8, 13))
        self.username = username
        self.sprite = None
        self.palette_index = palette_index
        self.load_sprite(palette_index)

        self.goal_position = pygame.Vector2(0, 0)
        self.current_particle = 0
        
        self.particle_emitter = ParticleEmitter(30)
        self.particle_timer = Timer(100)

        self.TAG_COLOR = graphics.PALETTE[6]
        self.TAG_SURF = graphics.FONT.render(self.username, antialias=False, color=(255, 255, 255))
        self.TAG_SURF.set_alpha(self.TAG_ALPHA)
        self.TAG_WIDTH = self.TAG_SURF.get_width()

    def load_sprite(self, palette_index):
        self.palette_index = palette_index
        self.sprite, _ = load_sprite(palette_index)
    
    def set_state(self, new_pos: pygame.Vector2, current_anim: int, current_particle: int, flip_x: bool, flash: bool, alpha: bool):
        self.goal_position = new_pos
        self.sprite.set_animation(Animations(current_anim))
        self.sprite.flip_x = flip_x
        self.current_particle = current_particle
        if flash:
            self.sprite.flash(100)
        if alpha:
            self.sprite.oscillate_alpha(100)

    def update(self):
        self.position = self.position.lerp(self.goal_position, 0.5)
        self.sprite.update(self.position)
        self.handle_particles()
    
    def render(self, display, offset):
        self.particle_emitter.render(display, offset)
        super().render(display, offset)

        if SETTINGS.get("show_gamertag"):
            display.blit(
                self.TAG_SURF, 
                (
                    self.position.x + self.TAG_OFFSET.x - self.TAG_WIDTH // 2 + offset.x, 
                    self.position.y + self.TAG_OFFSET.y + offset.y
                )
            )
    
    def handle_particles(self):
        self.particle_emitter.update()

        frame = self.sprite.frame
        if (frame == 2 or frame == 5) and self.sprite.frame_changed:
            self.particle_emitter.emit(StepParticle, self.position + pygame.Vector2(4, 14))

        if self.current_particle != 0:
            if self.particle_timer.is_done:
                if self.current_particle == 1:
                    self.particle_emitter.emit(
                        type=BoostUpParticle, 
                        position=self.position + pygame.Vector2(BOOST_OFFSET * self.sprite.flip_x, 7),
                        count=3
                    )
                elif self.current_particle == -1:
                    self.particle_emitter.emit(
                        type=BoostDownParticle, 
                        position=self.position + pygame.Vector2(BOOST_OFFSET * self.sprite.flip_x, 7),
                        count=3
                    )
                self.particle_timer.start()
