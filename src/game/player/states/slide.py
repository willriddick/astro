from src.util import State
from .player_state import PlayerState
from ..animation import Animation

class Slide(State):
    def __init__(self):
        super().__init__(PlayerState.SLIDE)
        self.timer = 0
    
    def on_enter(self):
        self.initial_x = 1 if self.owner.velocity.x > 0 else -1
        self.owner.velocity.x = self.owner.velocity.x * 1.5 #self.owner.slide_speed
        self.timer = 5

    def update(self):
        if self.owner.velocity.x == self.owner.ground_move_speed:
            self.switch(PlayerState.RUN)
        
        if self.owner.move_dir.y != 1:
            self.switch(PlayerState.RUN)
        

        self.timer = max(0, self.timer - 1)

        if self.timer == 0:
            self.owner.accelerate_x(self.initial_x, self.owner.ground_move_speed, (0.1, 0.1)) #self.owner.slide_acc) 

        self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)
        self.owner.handle_jump()
