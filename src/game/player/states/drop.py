from src.util import State 
from src.game.gravity import Gravity
from ..player import Player
from ..enums import Animations, States

class Drop(State):
    def __init__(self):
        super().__init__(States.DROP)
        self.dir = 0
    
    def on_enter(self):
        self.owner.sprite.set_next(Animations.DROP)
        self.dir = self.owner.move_dir.x

    def update(self):
        nearest = self.owner.collider.get_nearest(Gravity)
        if nearest:
            self.owner.gravity_multiplier = nearest.gravity_multiplier
            self.owner.velocity_multiplier.x = 0.9
        else:
            self.owner.gravity_multiplier = 1
            self.owner.velocity_multiplier.x = 1.0

        self.owner.apply_gravity(Player.DROP_GRAVITY, Player.DROP_FALL_SPEED * 2)
        self.owner.accelerate_x(self.dir, Player.AIR_MOVE_SPEED, Player.AIR_ACC)

        # switch states
        if not self.owner.drop_down:
            self.switch(States.AIR)

        if self.owner.on_ground:
            self.owner.camera.screenshake(20, 2)
            self.switch(States.SLIDE)
 