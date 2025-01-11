from src.util import State
from .player_state import PlayerState
from ..animation import Animation

class Slide(State):
    def __init__(self):
        super().__init__(PlayerState.SLIDE)
        self.timer = 0
    
    def on_enter(self):
        self.owner.set_animation(Animation.SLIDE)
        self.owner.slide_dir = 1 if self.owner.velocity.x > 0 else -1
        self.owner.velocity.x = self.owner.velocity.x * self.owner.initial_slide_multiplier
        self.entry_speed = abs(self.owner.velocity.x)
        self.timer = self.owner.slide_duration

    def update(self):
        self.owner.apply_gravity(self.owner.gravity, self.owner.fall_speed)
        self.owner.handle_jump()

        self.timer = max(0, self.timer - 1)
        goal_velocity = 0 if not self.timer else min(self.owner.slide_speed, self.entry_speed)
        self.owner.accelerate_x(self.owner.slide_dir, goal_velocity, self.owner.slide_acc)
    
        if (self.owner.velocity.x == self.owner.ground_move_speed
            or self.owner.move_dir.y != 1
        ):
            self.switch(PlayerState.RUN)
        
        if not self.owner.on_ground:
            self.switch(PlayerState.AIR)
