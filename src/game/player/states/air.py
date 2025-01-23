from src.util import State
from ..player import Player, Animation, PlayerState

class Air(State):
    def __init__(self):
        super().__init__(PlayerState.AIR)
    
    def on_enter(self):
        self.owner.sprite.set_next(Animation.AIR_UP if self.owner.velocity.y < 0 else Animation.AIR_DOWN)

    def update(self):
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.handle_jump()
        self.owner.handle_wall_jump()
        self.owner.accelerate_x(self.owner.move_dir.x, Player.AIR_MOVE_SPEED, Player.AIR_ACC)

        # handle rotation animation
        if self.owner.rotated:
            self.owner.sprite.set_animation_duration(Animation.FRONT, Player.AIR_ROTATE_DURATION)
        self.owner.sprite.set_next(Animation.AIR_UP if self.owner.velocity.y < 0 else Animation.AIR_DOWN)
        
        if self.owner.move_dir.x != 0:
            self.owner.sprite.flip = self.owner.move_dir.x == -1

        # switch states
        if self.owner.wall_slide_timer:
            self.switch(PlayerState.WALL_SLIDE)

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
 