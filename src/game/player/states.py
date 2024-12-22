from enum import Enum
from ...util import State

class PlayerState(Enum):
    IDLE = 0
    RUN = 1

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

class StateRun(State):
    def __init__(self):
        super().__init__('run', PlayerState.RUN)
    
    def on_enter(self):
        print('RUN ENTER')
    
    def update(self):
        if self.owner.move_dir == 0:
            self.owner.state_machine.switch(PlayerState.IDLE)
    
    def on_exit(self):
        print('RUN EXIT')

