from random import choice
from src.util import State
from src.util import approach
from .states import PlayerState

class StateWallJump(State):
    def __init__(self):
        super().__init__(PlayerState.WALL_JUMP)
        self.timer = 0
    
    def on_enter(self):
        self.timer = 20
    
    def update(self):
        self.timer = max(0, self.timer - 1)

        self.owner.velocity.x = approach(self.owner.velocity.x, self.owner.air_move_speed * -self.owner.wall_dir, 0.)
        self.owner.handle_gravity() 

        self.handle_animation()
        self.owner.handle_wall_jump()

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
        elif self.timer == 0:
            self.switch(PlayerState.AIR)
         
    def handle_animation(self):
        if self.owner.move_dir != 0 and self.owner.move_dir != self.owner.last_move_dir:
            self.owner.rotate_timer = self.owner.rotate_duration
            self.owner.rotate_dir = choice(self.owner.rotate_choice)
        
        if self.owner.move_dir != 0:
            self.owner.sprite.flip = self.owner.move_dir == -1
            self.owner.last_move_dir = self.owner.move_dir
        
        self.owner.rotate_timer = max(0, self.owner.rotate_timer - 1)
        
        animation = 'idle'
        if self.owner.rotate_timer > 0:
            if self.owner.rotate_dir:
                animation = 'front'
            else:
                animation = 'back'
        else:
            if self.owner.falling:
                animation = 'air_down'
            else:
                animation = 'air_up'
        
        self.owner.sprite.set_animation(animation)
    