from src.util import State
from ..player import Player
from ..enums import Animations, States

class Slide(State):
    def __init__(self):
        super().__init__(States.SLIDE)
        self.entry_speed = 0.0
        self.timer = 0

    def on_enter(self):
        self.owner.sprite.set_animation(Animations.SLIDE)
        self.owner.slide_dir = 1 if self.owner.velocity.x > 0 else -1
        self.owner.velocity.x = self.owner.velocity.x * Player.INITIAL_SLIDE_MULTIPLIER
        self.entry_speed = abs(self.owner.velocity.x)
        self.timer = Player.SLIDE_DURATION

    def update(self):
        self.timer = max(0, self.timer - 1)
        self.owner.handle_jump()

        goal_velocity = 0 if not self.timer else min(Player.SLIDE_SPEED, self.entry_speed)

        # if trying to move in opposite direction of slide
        if self.owner.move_dir.x != 0 and self.owner.move_dir.x != self.owner.slide_dir:
            # brake the slide
            self.owner.accelerate_x(self.owner.move_dir.x, goal_velocity, Player.SLIDE_ACC * 8)
        else:
            # continue sliding in the same direction
            self.owner.accelerate_x(self.owner.slide_dir, goal_velocity, Player.SLIDE_ACC)
    
        if (
            self.owner.velocity.x == Player.GROUND_MOVE_SPEED
            or self.owner.move_dir.y != 1
        ):
            self.switch(States.RUN)
        
        if not self.owner.on_ground and self.timer == 0:
            self.switch(States.AIR)
