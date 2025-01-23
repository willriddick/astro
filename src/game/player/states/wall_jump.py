from src.util import State 
from ..player import Player, PlayerState, Animation

class WallJump(State):
    def __init__(self):
        super().__init__(PlayerState.WALL_JUMP)
        self.timer = 0
    
    def on_enter(self):
        self.timer = Player.WALL_JUMP_DURATION
        self.owner.sprite.set_animation(Animation.AIR_UP)
        self.owner.sprite.flip = (self.owner.wall_slide_dir == 1)
        self.owner.velocity.x = Player.WALL_JUMP_SPEED.x * -self.owner.wall_slide_dir * self.owner.velocity_multiplier.x
        self.owner.velocity.y = -Player.WALL_JUMP_SPEED.y * self.owner.velocity_multiplier.y
        self.owner.jump_input_timer = 0
        self.owner.variable_jump_timer = Player.VARIABLE_JUMP_BUFFER
        self.owner.wall_slide_timer = 0
    
    def on_exit(self):
        self.owner.last_facing_dir = -self.owner.wall_slide_dir
    
    def update(self):
        self.timer = max(0, self.timer - 1)

        self.owner.accelerate_x(
            dir_ = -self.owner.wall_slide_dir, 
            max_speed = Player.AIR_MOVE_SPEED,
            acc = Player.AIR_ACC
        )

        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
        elif self.timer == 0:
            self.switch(PlayerState.AIR)
    