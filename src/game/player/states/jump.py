from src.util import State, Timer, Assets
from ..player import Player
from ..enums import States

class Jump(State):
    def __init__(self):
        super().__init__(States.JUMP)
        self.timer = Timer(5)
    
    def on_enter(self):
        # special case for coyote time 
        if (
            self.owner.jumps_remaining == Player.MAX_JUMPS 
            and not self.owner.on_ground and self.owner.coyote_timer.is_done
        ):
            self.owner.jumps_remaining -= 1
        
        # update velocity and jump count
        if self.owner.jumps_remaining:
            self.owner.jumps_remaining = max(0, self.owner.jumps_remaining - 1)

            self.owner.velocity.y = -Player.JUMP_SPEED * self.owner.velocity_multiplier.y
            self.owner.jump_input_timer.reset()
            self.owner.coyote_timer.reset()
            self.owner.variable_jump_timer.start()
        
        Assets.SOUNDS['jump'].play()
        
        # switch to AIR
        self.timer.start()
    
    def update(self):
        if self.timer.is_done:
            self.switch(States.AIR)
   