from random import choice
from src.util import State
from .states import PlayerState

class StateAir(State):
    def __init__(self):
        super().__init__('air', PlayerState.AIR)
    
    def update(self):
        self.owner.handle_movement(self.owner.air_move_speed, self.owner.air_acc)
        self.owner.handle_gravity()
        self.handle_animation()
        
        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
         
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
            if self.owner.velocity.y > 0:
                animation = 'air_down'
            else:
                animation = 'air_up'
        
        self.owner.sprite.set_animation(animation)
    