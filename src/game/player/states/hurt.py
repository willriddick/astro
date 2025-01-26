from src.util import State, Direction
from ..enums import States

class Hurt(State):
    def __init__(self):
        super().__init__(States.HURT)
    
    def on_enter(self):
        self.owner.sprite.flash(5)
        self.owner.sprite.oscillate_alpha(self.owner.health_component.invulnerable_duration, 3)
        self.owner.apply_force(2, Direction.UP)
        self.owner.camera.screenshake(10, 5)
        self.owner.set_state(self.owner.state_machine.previous_state.id)
