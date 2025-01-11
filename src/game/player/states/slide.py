from src.util import State
from ..player import Player, PlayerState, Animation

class Slide(State):
    def __init__(self):
        super().__init__(PlayerState.SLIDE)
        self.timer = 0
    
    def on_enter(self):
        self.owner.set_animation(Animation.SLIDE)
        self.owner.slide_dir = 1 if self.owner.velocity.x > 0 else -1
        self.owner.velocity.x = self.owner.velocity.x * Player.INITIAL_SLIDE_MULTIPLIER
        self.entry_speed = abs(self.owner.velocity.x)
        self.timer = Player.SLIDE_DURATION

    def update(self):
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.handle_jump()

        self.timer = max(0, self.timer - 1)
        goal_velocity = 0 if not self.timer else min(Player.SLIDE_SPEED, self.entry_speed)
        self.owner.accelerate_x(self.owner.slide_dir, goal_velocity, Player.SLIDE_ACC)
    
        if (self.owner.velocity.x == Player.GROUND_MOVE_SPEED
            or self.owner.move_dir.y != 1
        ):
            self.switch(PlayerState.RUN)
        
        if not self.owner.on_ground:
            self.switch(PlayerState.AIR)
