from src.util import State, approach
from .states import PlayerState

class StateWallJump(State):
    def __init__(self):
        super().__init__(PlayerState.WALL_JUMP)
        self.timer = 0
    
    def on_enter(self):
        self.timer = self.owner.wall_jump_duration
        self.owner.sprite.set_animation('air_up')
        self.owner.sprite.flip = (self.owner.slide_dir == 1)
    
    def on_exit(self):
        self.owner.last_move_dir = -self.owner.slide_dir
    
    def update(self):
        self.timer = max(0, self.timer - 1)

        self.owner.velocity.x = approach(
            self.owner.velocity.x,
            self.owner.air_move_speed * -self.owner.slide_dir,
            self.owner.wall_jump_dec
        )

        self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
        elif self.timer == 0:
            self.switch(PlayerState.AIR)
    