from src.util import State
from .states import PlayerState

class StateIdle(State):
    def __init__(self):
        super().__init__('idle', PlayerState.IDLE)
    
    def on_enter(self):
        print('IDLE ENTER')
    
    def update(self):
        if self.owner.move_dir != 0:
            self.owner.state_machine.switch(PlayerState.RUN)
    
    def on_exit(self):
        print('IDLE EXIT')
