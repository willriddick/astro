from src.util import State, Direction, Assets
from ..enums import States

class Hurt(State):
    def __init__(self):
        super().__init__(States.HURT)
    
    def on_enter(self):
        Assets.SOUNDS['hurt'].play()
        self.owner.sprite.flash(100)
        self.owner.sprite.oscillate_alpha(self.owner.health_component.invulnerable_duration, speed=125)
        self.owner.apply_force(100, Direction.UP)
        self.owner.camera.screenshake(30, 10)
        self.owner.set_state(self.owner.state_machine.previous_state.id)
