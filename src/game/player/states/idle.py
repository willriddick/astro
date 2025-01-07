from src.util import State
from .player_state import PlayerState
from ..animation import Animation

class Idle(State):
    def __init__(self):
        super().__init__(PlayerState.IDLE)
    
    def on_enter(self):
        self.owner.set_animation(Animation.IDLE)
    
    def update(self):
        self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)
        self.owner.handle_jump()

        if self.owner.move_dir.x != 0:
            self.switch(PlayerState.RUN)
        
        if not self.owner.on_ground:
            self.switch(PlayerState.AIR)
    