from src.util import State 
from ..player import Player
from ..enums import Animations, States

class Drop(State):
    def __init__(self):
        super().__init__(States.DROP)
        self.dir = 0
    
    def on_enter(self):
        self.owner.sprite.set_next(Animations.DROP)
        self.dir = self.owner.input_dir.x

    def update(self):
        self.owner.apply_gravity(Player.DROP_GRAVITY, Player.DROP_FALL_SPEED)
        self.owner.accelerate_x(self.dir, Player.AIR_MOVE_SPEED, Player.AIR_ACC)

        # switch states
        if not self.owner.input_dir.y == 1:
            self.switch(States.AIR)

        if self.owner.on_ground:
            self.switch(States.SLIDE)
 