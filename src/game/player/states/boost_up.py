from src.util import State, approach, Assets
from src.game.clock import Clock
from ..player import Player
from ..enums import Animations, States

class BoostUp(State):
    def __init__(self):
        super().__init__(States.BOOST_UP)
        self.dir = 0
    
    def on_enter(self):
        Assets.SOUNDS.play('boost')
        self.owner.sprite.set_next(Animations.BOOST_UP)
        self.owner.velocity.y = min(self.owner.velocity.y, -Player.INITIAL_BOOST_UP)
    
    def on_exit(self):
        self.owner.refuel_timer.start()
    
    def update(self):
        self.owner.accelerate_x(self.owner.input_dir.x, Player.BOOST_MOVE_SPEED, Player.BOOST_MOVE_ACC)

        self.owner.fuel = approach(self.owner.fuel, 0, 100 * Clock.dt())
        self.owner.accelerate_y(-1, Player.BOOST_SPEED, (Player.BOOST_ACC, Player.BOOST_ACC))
        self.owner.velocity.y = max(self.owner.velocity.y, -Player.BOOST_SPEED)

        # switch states
        if self.owner.input_dir.y != -1:
            self.switch(States.AIR)
        
        if self.owner.fuel <= 0:
            self.switch(States.AIR)
        