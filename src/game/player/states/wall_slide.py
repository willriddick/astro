from src.util import State, Direction
from ..player import Player, PlayerState, Animation

class WallSlide(State):
    def __init__(self):
        super().__init__(PlayerState.WALL_SLIDE)

    def on_enter(self):
        self.owner.sprite.flip = (self.owner.wall_slide_dir == 1)
        self.owner.set_animation(Animation.WALL_SLIDE)
    
    def on_exit(self):
        self.owner.last_rotate_dir = -self.owner.wall_slide_dir
        self.owner.slide_left_timer = 0
        self.owner.slide_right_timer = 0
    
    def update(self):
        self.owner.accelerate_x(self.owner.move_dir.x, Player.AIR_MOVE_SPEED, Player.AIR_ACC)
        self.owner.handle_wall_jump()

        if self.owner.velocity.y < 0 or self.owner.move_dir.x != self.owner.wall_slide_dir:
            self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        else:
            self.owner.apply_gravity(Player.WALL_SLIDE_GRAVITY, Player.WALL_SLIDE_SPEED)
            self.owner.set_animation(Animation.WALL_SLIDE)
        
        if self.owner.move_dir.x != self.owner.wall_slide_dir:
            self.owner.set_animation(Animation.AIR_DOWN if self.owner.falling else Animation.AIR_UP)

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
        
        if (
            (self.owner.wall_slide_dir == -1 and not self.owner.collisions[Direction.LEFT])
            or (self.owner.wall_slide_dir == 1 and not self.owner.collisions[Direction.RIGHT])
        ):
            self.switch(PlayerState.AIR)
        