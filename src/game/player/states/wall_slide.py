from src.util import State, Direction
from .states import PlayerState

class StateWallSlide(State):
    def __init__(self):
        super().__init__(PlayerState.WALL_SLIDE)

    def on_enter(self):
        self.owner.sprite.flip = (self.owner.slide_dir == 1)
        self.owner.sprite.set_animation('idle')
    
    def on_exit(self):
        self.owner.last_move_dir = -self.owner.slide_dir
    
    def update(self):
        self.owner.apply_movement(self.owner.air_move_speed, self.owner.air_acc)

        if self.owner.velocity.y < 0 or self.owner.move_dir != self.owner.slide_dir:
            self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)
        else:
            self.owner.apply_gravity(self.owner.wall_slide_gravity, self.owner.wall_slide_speed)
        
        self.owner.handle_wall_jump()

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
        
        if not self.owner.collisions[Direction.LEFT] and not self.owner.collisions[Direction.RIGHT]:
            self.owner.pressed_left_timer = 0
            self.owner.pressed_right_timer = 0
            self.switch(PlayerState.AIR)
        