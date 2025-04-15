import pygame
from src.util import State, Direction
from src.sounds import SOUNDS
from src.camera import CAMERA
from src.particles import HurtParticle
from ..enums import States

class Hurt(State):
    def __init__(self):
        super().__init__(States.HURT)
    
    def on_enter(self):
        SOUNDS.play('hurt')
        self.owner.sprite.flash(100)
        self.owner.sprite.oscillate_alpha(self.owner.health_component.invulnerable_duration, speed=125)
        self.owner.apply_force(100, Direction.UP)
        CAMERA.screenshake(30, 10)

        self.owner.particle_emitter.emit(
            type=HurtParticle, 
            position=self.owner.position + pygame.Vector2(4, 12),
            count=7
        )

        self.owner.set_state(self.owner.state_machine.previous_state.id)
