import pygame
from src.util import State, Direction
from ..player import Player
from ..enums import Animations, States

class Hurt(State):
    def __init__(self):
        super().__init__(States.HURT)
    
    def on_enter(self):
        self.owner.sprite.flash(5)
        self.owner.sprite.oscillate_alpha(self.owner.health_component.invulnerable_duration, 2)
        self.owner.apply_force(2, Direction.UP)
        self.owner.set_state(self.owner.state_machine.previous_state.id)
