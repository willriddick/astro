from src.util import State, Timer
from ..player import Player
from ..enums import Animations, States

class Slide(State):
    def __init__(self):
        super().__init__(States.SLIDE)
        self.entry_speed = 0.0
        self.timer = Timer(Player.SLIDE_DURATION)

    def on_enter(self):
        self.owner.sprite.set_animation(Animations.SLIDE)
        self.owner.slide_dir = 1 if self.owner.velocity.x > 0 else -1
        self.owner.velocity.x = self.owner.velocity.x * Player.INITIAL_SLIDE_MULTIPLIER
        self.entry_speed = abs(self.owner.velocity.x)
        self.owner.camera.screenshake(10, 3)
        self.timer.start()

    def update(self):
        self.owner.handle_jump()

        goal_velocity = 0 if self.timer.is_done else min(Player.SLIDE_SPEED, self.entry_speed)
        self.owner.accelerate_x(self.owner.slide_dir, goal_velocity, Player.SLIDE_ACC)
    
        if self.owner.move_dir.y != 1:
            self.switch(States.RUN)
        
        if not self.owner.on_ground and self.timer.is_done:
            self.switch(States.AIR)
