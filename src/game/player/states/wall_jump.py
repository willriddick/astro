from random import choice
from src.util import State
from src.util import approach
from .states import PlayerState

class StateWallJump(State):
    def __init__(self):
        super().__init__(PlayerState.WALL_JUMP)
        self.timer = 0
    
    def on_enter(self):
        self.timer = 10
        self.owner.sprite.set_animation('air_up')
        self.owner.sprite.flip = self.owner.wall_dir == 1
    
    def update(self):
        self.timer = max(0, self.timer - 1)

        self.owner.velocity.x = approach(self.owner.velocity.x, self.owner.air_move_speed * -self.owner.wall_dir, 0.05)
        self.owner.handle_gravity() 

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
        elif self.timer == 0:
            self.switch(PlayerState.AIR)
    