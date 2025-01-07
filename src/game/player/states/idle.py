from src.util import State
from .states import States
from ..animation import Animation

class Idle(State):
    def __init__(self):
        super().__init__(States.IDLE)
    
    def on_enter(self):
        self.owner.set_animation(Animation.IDLE)
    
    def update(self):
        self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)
        self.owner.handle_jump()

        if self.owner.move_dir.x != 0:
            self.switch(States.RUN)
        
        if not self.owner.on_ground:
            self.switch(States.AIR)
    