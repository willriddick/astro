from src.util import State 
from .player_state import PlayerState
from ..animation import Animation

class WallJump(State):
    def __init__(self):
        super().__init__(PlayerState.WALL_JUMP)
        self.timer = 0
    
    def on_enter(self):
        self.timer = self.owner.wall_jump_duration
        self.owner.set_animation(Animation.AIR_UP)
        self.owner.sprite.flip = (self.owner.wall_slide_dir == 1)
        self.owner.velocity.x = self.owner.wall_jump_speed[0] * -self.owner.wall_slide_dir * self.owner.velocity_multiplier.x
        self.owner.velocity.y = -self.owner.wall_jump_speed[1] * self.owner.velocity_multiplier.y
        self.owner.jump_input_timer = 0
        self.owner.wall_slide_timer = 0
    
    def on_exit(self):
        self.owner.last_rotate_dir = -self.owner.wall_slide_dir
    
    def update(self):
        self.timer = max(0, self.timer - 1)

        self.owner.accelerate_x(
            dir_ = -self.owner.wall_slide_dir, 
            max_speed = self.owner.air_move_speed,
            acc = self.owner.wall_jump_acc
        )

        self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
        elif self.timer == 0:
            self.switch(PlayerState.AIR)
    