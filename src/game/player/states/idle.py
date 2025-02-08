from src.util import State, Timer
from ..player import Player
from ..enums import Animations, States

class Idle(State):
    def __init__(self):
        super().__init__(States.IDLE)
        self.animation_timer = Timer(30)
    
    def on_enter(self):
        self.animation_timer.start()
        self.owner.sprite.set_next(Animations.IDLE_A)
    
    def update(self):
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.handle_jump()

        if self.animation_timer.is_done:
            self.owner.sprite.set_animation(Animations.IDLE_B)

        if self.owner.input_dir.x != 0:
            self.switch(States.RUN)
        
        if not self.owner.on_ground:
            self.switch(States.AIR)
