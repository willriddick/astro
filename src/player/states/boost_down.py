import pygame
from src.util import State, Timer
from src.sounds import SOUNDS
from src.camera import CAMERA
from src.particles import BoostDownParticle
from ..player import Player
from ..enums import Animations, States


BOOST_OFFSET = 9


class BoostDown(State):
    def __init__(self):
        super().__init__(States.BOOST_DOWN)
        self.dir = 0
        self.timer = Timer(100)
    
    def on_enter(self):
        SOUNDS.play('boost')
        self.owner.velocity.y = max(self.owner.velocity.y + Player.INITIAL_BOOST_DOWN, Player.INITIAL_BOOST_DOWN)
        self.owner.fuel -= Player.BOOST_DOWN_COST
        self.owner.sprite.set_next(Animations.BOOST_DOWN)
        self.dir = self.owner.input_dir.x

        self.owner.particle_emitter.emit(
            type=BoostDownParticle, 
            position=self.owner.position + pygame.Vector2(BOOST_OFFSET * self.owner.sprite.flip_x, 7),
            count=5
        )
        self.owner.current_particle = -1

    def on_exit(self):
        self.owner.refuel_timer.start()
        self.owner.current_particle = 0

    def update(self):
        self.owner.apply_gravity(Player.GRAVITY, Player.BOOST_DOWN_SPEED)
        self.owner.accelerate_x(self.dir, Player.BOOST_DOWN_MOVE_SPEED, Player.BOOST_DOWN_MOVE_ACC)

        CAMERA.screenshake(1, 0.3)

        # emit particles
        if self.timer.is_done:
            self.owner.particle_emitter.emit(
                type=BoostDownParticle, 
                position=self.owner.position + pygame.Vector2(BOOST_OFFSET * self.owner.sprite.flip_x, 7),
                count=2
            )
            self.timer.start()

        # switch states
        if not self.owner.input_dir.y == 1:
            self.switch(States.AIR)

        if self.owner.on_ground:
            self.switch(States.SLIDE)
 