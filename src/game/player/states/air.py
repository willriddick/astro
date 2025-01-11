from random import choice
from src.util import State
from ..player import Player, Animation, PlayerState

class Air(State):
    def __init__(self):
        super().__init__(PlayerState.AIR)
    
    def update(self):
        self.owner.accelerate_x(self.owner.move_dir.x, Player.AIR_MOVE_SPEED, Player.AIR_ACC)
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.handle_jump()
        self.owner.handle_wall_jump()
        self.handle_animation()

        if self.owner.wall_slide_timer:
            self.switch(PlayerState.WALL_SLIDE)

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
         
    def handle_animation(self):
        move_dir = self.owner.move_dir.x
        if move_dir != 0 and move_dir != self.owner.last_facing_dir:
            self.owner.rotate_dir = choice(Player.ROTATE_CHOICE)
            self.owner.sprite.set_animation_duration(Animation.FRONT, Player.ROTATE_DURATION)
        
        if move_dir != 0:
            self.owner.sprite.flip = move_dir == -1
            self.owner.last_facing_dir = move_dir
        
        self.owner.sprite.set_next(Animation.AIR_DOWN if self.owner.falling else Animation.AIR_UP)
