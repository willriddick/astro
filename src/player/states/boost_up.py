import pygame
from src.util import State, approach, Timer
from src.clock import CLOCK
from src.sounds import SOUNDS
from src.particles import BoostUpParticle
from ..player import Player
from ..enums import Animations, States


class BoostUp(State):
    def __init__(self):
        super().__init__(States.BOOST_UP)
        self.dir = 0
        self.timer = Timer(100)
    
    def on_enter(self):
        SOUNDS.play('boost')
        self.owner.fuel -= Player.BOOST_UP_COST
        self.owner.sprite.set_next(Animations.BOOST_UP)
        self.owner.velocity.y = min(self.owner.velocity.y, -Player.INITIAL_BOOST_UP)
    
    def on_exit(self):
        self.owner.refuel_timer.start()
    
    def update(self):
        self.owner.accelerate_x(self.owner.input_dir.x, Player.BOOST_UP_MOVE_SPEED, Player.BOOST_UP_MOVE_ACC)

        self.owner.fuel = approach(self.owner.fuel, 0, 100 * CLOCK.dt)
        self.owner.accelerate_y(-1, Player.BOOST_UP_SPEED, (Player.BOOST_ACC, Player.BOOST_ACC))
        self.owner.velocity.y = max(self.owner.velocity.y, -Player.BOOST_UP_SPEED)
        self.owner.handle_wall_jump()

        # emit particles
        if self.timer.is_done:
            self.owner.particle_emitter.emit(
                type=BoostUpParticle, 
                position=self.owner.position + pygame.Vector2(6, 4),
                count=3
            )
            self.timer.start()

        # switch states
        if self.owner.input_dir.y != -1:
            self.switch(States.AIR)
        
        if self.owner.fuel <= 0:
            self.switch(States.AIR)
        