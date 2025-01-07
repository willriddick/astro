from src.util import State
from .player_state import PlayerState

class Jump(State):
    def __init__(self):
        super().__init__(PlayerState.JUMP)
    
    def on_enter(self):
        # Special case for coyote time
        if self.owner.jumps_remaining == self.owner.max_jumps and not self.owner.on_ground and self.owner.coyote_timer == 0:
            self.owner.jumps_remaining -= 1
        
        # Decrement remaining jumps
        if self.owner.jumps_remaining:
            self.owner.jumps_remaining = max(0, self.owner.jumps_remaining - 1)

            self.owner.velocity.y = -self.owner.jump_speed * self.owner.velocity_multiplier.y
            self.owner.jump_input_timer = 0
            self.owner.coyote_timer = 0
            self.owner.variable_jump_timer = self.owner.variable_jump_buffer
        
        self.switch(PlayerState.AIR)
   