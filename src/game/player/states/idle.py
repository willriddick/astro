from src.util import State
from ..player import Player
from ..enums import Animations, States

class Idle(State):
    def __init__(self):
        super().__init__(States.IDLE)
        self.timer = 0
    
    def on_enter(self):
        self.timer = 0
        self.owner.sprite.set_next(Animations.IDLE_A)
    
    def update(self):
        self.timer = max(0, self.timer + 1)

        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.handle_jump()

        if self.timer >= 30:
            self.owner.sprite.set_animation(Animations.IDLE_B)

        if self.owner.move_dir.x != 0:
            self.switch(States.RUN)
        
        if not self.owner.on_ground:
            self.switch(States.AIR)
