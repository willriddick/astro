from src.util import State
from .states import States

class Jump(State):
    def __init__(self):
        super().__init__(States.JUMP)
    
    def on_enter(self):
        # Special case for coyote time
        if self.owner.jumps_remaining == self.owner.max_jumps and not self.owner.on_ground and self.owner.coyote_timer == 0:
            self.owner.jumps_remaining -= 1
        
        # Decrement remaining jumps
        if self.owner.jumps_remaining:
            self.owner.jumps_remaining = max(0, self.owner.jumps_remaining - 1)

            self.owner.velocity.y = -self.owner.jump_speed
            self.owner.jump_input_timer = 0
            self.owner.coyote_timer = 0
            self.owner.variable_jump_timer = self.owner.variable_jump_buffer
        
        self.switch(States.AIR)
   