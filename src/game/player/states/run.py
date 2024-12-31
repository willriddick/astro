from random import choice
from src.util import State
from .states import States
from ..animation import Animation

class Run(State):
    def __init__(self):
        super().__init__(States.RUN)
    
    def update(self):
        self.owner.accelerate_x(self.owner.move_dir, self.owner.ground_move_speed, self.owner.ground_acc)
        self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)
        self.owner.handle_jump()
        self.handle_animation()
        
        if self.owner.velocity.x == 0:
            self.switch(States.IDLE)
        
        if not self.owner.on_ground:
            self.switch(States.AIR)
        
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
        elif self.owner.move_dir != 0:
            animation = Animation.RUN
        
        self.owner.set_animation(animation)
