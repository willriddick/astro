from random import choice
from src.util import State
from .states import PlayerState

class StateAir(State):
    def __init__(self):
        super().__init__(PlayerState.AIR)
    
    def update(self):
        self.owner.handle_movement(self.owner.air_move_speed, self.owner.air_acc)

        self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)

        self.owner.variable_jump_timer = max(0, self.owner.variable_jump_timer - 1)
        if not self.owner.holding_jump and self.owner.variable_jump_timer > 0 and self.owner.velocity.y < 0:
            self.owner.velocity.y *= (self.owner.variable_jump_multiplier / (1 / self.owner.gravity_multiplier))

        self.owner.handle_wall_jump()
        self.handle_animation()

        if self.owner.slide_left_timer or self.owner.slide_right_timer:
            self.switch(PlayerState.WALL_SLIDE)

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
            if self.owner.falling:
                animation = 'air_down'
            else:
                animation = 'air_up'
        
        self.owner.sprite.set_animation(animation)
    