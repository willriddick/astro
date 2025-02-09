from src.util import State, Timer, approach
from ..player import Player
from ..enums import Animations, States

class BoostUp(State):
    def __init__(self):
        super().__init__(States.BOOST_UP)
        self.dir = 0
    
    def on_enter(self):
        self.owner.sprite.set_next(Animations.DROP)
        self.dir = self.owner.input_dir.x
    
    def on_exit(self):
        self.owner.just_boosted_timer.start()

    def update(self):
        self.owner.velocity.y = approach(self.owner.velocity.y, -200, 0.5)
        self.owner.accelerate_x(self.dir, Player.AIR_MOVE_SPEED, Player.AIR_ACC)

        # switch states
        if self.owner.on_ground:
            self.switch(States.SLIDE)
        
        if self.owner.input_dir.y != -1:
            self.switch(States.AIR)
        