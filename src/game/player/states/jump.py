from src.util import State
from ..player import Player, PlayerState

class Jump(State):
    def __init__(self):
        super().__init__(PlayerState.JUMP)
    
    def on_enter(self):
        # Special case for coyote time
        if (self.owner.jumps_remaining == Player.MAX_JUMPS 
            and not self.owner.on_ground and self.owner.coyote_timer == 0
        ):
            self.owner.jumps_remaining -= 1
        
        # Decrement remaining jumps
        if self.owner.jumps_remaining:
            self.owner.jumps_remaining = max(0, self.owner.jumps_remaining - 1)

            self.owner.velocity.y = -Player.JUMP_SPEED * self.owner.velocity_multiplier.y
            self.owner.jump_input_timer = 0
            self.owner.coyote_timer = 0
            self.owner.variable_jump_timer = Player.VARIABLE_JUMP_BUFFER
        
        self.switch(PlayerState.AIR)
   