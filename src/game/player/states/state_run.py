from math import copysign 
from random import choice
from src.util import State
from .states import PlayerState

class StateRun(State):
    def __init__(self):
        super().__init__('run', PlayerState.RUN)
    
    def on_enter(self):
        print('RUN ENTER')
    
    def update(self):
        # Update x velocity
        acc = self.owner.ground_acc if self.owner.on_ground else self.owner.air_acc
        if self.owner.move_dir == 0:
            # Apply deceleration
            if abs(self.owner.velocity.x) < acc[1]:
                self.owner.velocity.x = 0
            else:
                # Copysign returns the first argument with the sign of the second argument
                self.owner.velocity.x -= copysign(acc[1], self.owner.velocity.x)
        else:
            # Apply acceleration, clamping velocity to the move speed
            self.owner.velocity.x = max(
                -self.owner.move_speed, 
                min(self.owner.move_speed, self.owner.velocity.x + (self.owner.move_dir * acc[0])))
        
        self.handle_animation()

        if self.owner.velocity.x == 0:
            self.switch(PlayerState.IDLE)
    
    def on_exit(self):
        print('RUN EXIT')
    
    def handle_animation(self):
        # Update rotate timer
        self.owner.rotate_timer = max(0, self.owner.rotate_timer - 1)

        # Detect direction change
        if self.owner.move_dir != 0 and self.owner.move_dir != self.owner.last_move_dir:
            self.owner.rotate_timer = self.owner.rotate_duration
            self.owner.rotate_dir = choice(self.owner.rotate_choice)
        
        # Handle flip
        if self.owner.move_dir != 0:
            self.owner.sprite.flip = self.owner.move_dir == -1
        
        if self.owner.rotate_timer > 0:
            if self.owner.rotate_dir:
                self.owner.sprite.set_animation('front')
            else:
                self.owner.sprite.set_animation('back')
        elif self.owner.move_dir != 0:
            self.owner.sprite.set_animation('run')
        else:
            self.owner.sprite.set_animation('idle')
