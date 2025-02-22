from src.util import State, Timer
from src.sounds import SOUNDS
from ..player import Player
from ..enums import Animations, States

class WallJump(State):
    def __init__(self):
        super().__init__(States.WALL_JUMP)
        self.timer = Timer(Player.WALL_JUMP_DURATION)
    
    def on_enter(self):
        self.timer.start()

        SOUNDS.play('wall_jump', pitch_index=self.owner.consecutive_wall_jumps)
        self.owner.consecutive_wall_jumps += 1

        self.owner.sprite.set_animation(Animations.AIR_UP)
        self.owner.sprite.flip_x = (self.owner.wall_slide_dir == 1)
        self.owner.velocity.x = Player.WALL_JUMP_SPEED.x * -self.owner.wall_slide_dir * self.owner.velocity_multiplier.x
        self.owner.velocity.y = -Player.WALL_JUMP_SPEED.y * self.owner.velocity_multiplier.y
        self.owner.jump_input_timer.reset()
        self.owner.variable_jump_timer.start()
        self.owner.wall_slide_timer.reset()
    
    def on_exit(self):
        self.owner.last_facing_dir = -self.owner.wall_slide_dir
    
    def update(self):
        self.owner.accelerate_x(
            dir_ = -self.owner.wall_slide_dir, 
            speed = Player.AIR_MOVE_SPEED,
            acc = Player.AIR_ACC
        )

        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(States.IDLE)
            else:
                self.switch(States.RUN)
        elif self.timer.is_done:
            self.switch(States.AIR)
    