from src.util import State
from .states import PlayerState

class StateIdle(State):
    def __init__(self):
        super().__init__(PlayerState.IDLE)
    
    def on_enter(self):
        self.owner.sprite.set_animation('idle')
    
    def update(self):
        self.owner.handle_jump()

        if self.owner.move_dir != 0:
            self.switch(PlayerState.RUN)
        
        if not self.owner.on_ground:
            self.switch(PlayerState.AIR)
    