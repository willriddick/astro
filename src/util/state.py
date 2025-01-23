from enum import Enum

class State:
    def __init__(self, _id: Enum):
        self.id = _id
        self.state_machine = None
    
    def switch(self, _id: Enum):
        if self.state_machine is None:
            raise ValueError('State machine is not set.')
        self.state_machine.switch(_id)
    
    @property
    def name(self):
        return self.id.name
 
    @property
    def owner(self):
        if self.state_machine is None:
            raise ValueError('State machine is not set.')
        return self.state_machine.owner

    def on_enter(self):
        pass
    
    def update(self):
        pass

    def on_exit(self):
        pass
    