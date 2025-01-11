from src.util import State, Direction
from .player_state import PlayerState
from ..animation import Animation

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
        self.owner.accelerate_x(self.owner.move_dir.x, self.owner.air_move_speed, self.owner.air_acc)

        if self.owner.velocity.y < 0 or self.owner.move_dir.x != self.owner.wall_slide_dir:
            self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)
        else:
            self.owner.apply_gravity(self.owner.wall_slide_gravity, self.owner.wall_slide_speed)
        
        self.owner.handle_wall_jump()

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
        
        if (
            (self.owner.wall_slide_dir == -1 and not self.owner.collisions[Direction.LEFT])
            or (self.owner.wall_slide_dir == 1 and not self.owner.collisions[Direction.RIGHT])
            or (self.owner.move_dir.x != self.owner.wall_slide_dir)
            or (self.owner.move_dir.x == 0)
        ):
            self.switch(PlayerState.AIR)
        