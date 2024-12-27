from random import choice
from src.util import State
from .states import States
from ..animation import Animation

class Air(State):
    def __init__(self):
        super().__init__(States.AIR)
    
    def update(self):
        self.owner.apply_movement(self.owner.move_dir, self.owner.air_move_speed, self.owner.air_acc)
        self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)
        self.owner.handle_jump()

        self.owner.variable_jump_timer = max(0, self.owner.variable_jump_timer - 1)
        if not self.owner.holding_jump and self.owner.variable_jump_timer > 0 and self.owner.velocity.y < 0:
            self.owner.velocity.y *= (self.owner.variable_jump_multiplier / (1 / self.owner.gravity_multiplier))

        self.owner.handle_wall_jump()
        self.handle_animation()

        if self.owner.slide_timer:
            self.switch(States.WALL_SLIDE)

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(States.IDLE)
            else:
                self.switch(States.RUN)
         
    def handle_animation(self):
        if self.owner.move_dir != 0 and self.owner.move_dir != self.owner.last_move_dir:
            self.owner.rotate_timer = self.owner.rotate_duration
            self.owner.rotate_dir = choice(self.owner.rotate_choice)
        
        if self.owner.move_dir != 0:
            self.owner.sprite.flip = self.owner.move_dir == -1
            self.owner.last_move_dir = self.owner.move_dir
        
        self.owner.rotate_timer = max(0, self.owner.rotate_timer - 1)
        
        animation = Animation.IDLE
        if self.owner.rotate_timer > 0:
            animation = Animation.FRONT if self.owner.rotate_dir else Animation.BACK
        else:
            animation = Animation.AIR_DOWN if self.owner.falling else Animation.AIR_UP
        
        self.owner.set_animation(animation)
    