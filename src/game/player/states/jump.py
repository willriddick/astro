from src.util import State
from .states import States

class Jump(State):
    def __init__(self):
        super().__init__(States.JUMP)
    
    def on_enter(self):
        self.owner.velocity.y = -self.owner.jump_speed
        self.owner.jump_input_timer = 0
        self.owner.coyote_timer = 0
        self.owner.variable_jump_timer = self.owner.variable_jump_buffer
        self.switch(States.AIR)
   