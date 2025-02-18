from src.util import State, Timer, Assets
from ..player import Player
from ..enums import Animations, States

class Slide(State):
    def __init__(self):
        super().__init__(States.SLIDE)
        self.entry_speed = 0.0
        self.timer = Timer(Player.SLIDE_DURATION)

    def on_enter(self):
        Assets.SOUNDS.play('slide')
        self.owner.sprite.set_animation(Animations.SLIDE)
        self.owner.camera.screenshake(20, 2)
        self.owner.slide_dir = self.owner.last_facing_dir

        if self.owner.velocity.x == 0:
            self.owner.velocity.x = self.owner.slide_dir * Player.INITIAL_SLIDE_SPEED
        else:
            self.owner.velocity.x = self.owner.velocity.x * Player.INITIAL_SLIDE_MULTIPLIER

        self.entry_speed = abs(self.owner.velocity.x)
        self.timer.start()

    def update(self):
        goal_velocity = 0 if self.timer.is_done else min(Player.SLIDE_SPEED, self.entry_speed)
        self.owner.accelerate_x(self.owner.slide_dir, goal_velocity, Player.SLIDE_ACC)
    
        if self.owner.input_dir.y != 1:
            self.switch(States.RUN)

        if not self.owner.on_ground and self.timer.is_done:
            self.switch(States.AIR)
        
        self.owner.handle_jump()
