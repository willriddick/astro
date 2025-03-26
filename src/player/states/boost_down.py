import pygame
from src.util import State
from src.sounds import SOUNDS
from src.particles import BoostDownParticle
from ..player import Player
from ..enums import Animations, States


class BoostDown(State):
    def __init__(self):
        super().__init__(States.BOOST_DOWN)
        self.dir = 0
    
    def on_enter(self):
        SOUNDS.play('boost')
        self.owner.velocity.y = max(self.owner.velocity.y + Player.INITIAL_BOOST_DOWN, Player.INITIAL_BOOST_DOWN)
        self.owner.fuel -= Player.BOOST_DOWN_COST
        self.owner.sprite.set_next(Animations.BOOST_DOWN)
        self.dir = self.owner.input_dir.x

        self.owner.particle_emitter.emit(
            type=BoostDownParticle, 
            position=self.owner.position + pygame.Vector2(6, 10),
            count=15
        )
    
    def on_exit(self):
        self.owner.refuel_timer.start()

    def update(self):
        self.owner.apply_gravity(Player.GRAVITY, Player.BOOST_DOWN_SPEED)
        self.owner.accelerate_x(self.dir, Player.BOOST_DOWN_MOVE_SPEED, Player.BOOST_DOWN_MOVE_ACC)

        # switch states
        if not self.owner.input_dir.y == 1:
            self.switch(States.AIR)

        if self.owner.on_ground:
            self.switch(States.SLIDE)
 