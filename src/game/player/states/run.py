from src.util import State
from ..player import Player
from ..enums import Animations, States

class Run(State):
    def __init__(self):
        super().__init__(States.RUN)
        self.timer = 0

    def on_enter(self):
        self.timer = 0 # duration player has been in RUN state
        self.owner.sprite.set_next(Animations.RUN)
        if self.owner.rotated:
            self.owner.sprite.set_animation_duration(Animations.FRONT, Player.ROTATE_DURATION, Animations.RUN)
        
    def update(self):
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.accelerate_x(self.owner.move_dir.x, Player.GROUND_MOVE_SPEED, Player.GROUND_ACC)
        self.owner.handle_jump()

        # animate player
        if self.owner.rotated:
            self.owner.sprite.set_animation_duration(Animations.FRONT, Player.ROTATE_DURATION, Animations.RUN)
        
        if self.owner.move_dir.x != 0:
            self.owner.sprite.flip = self.owner.move_dir.x == -1

        # switch to slide state
        self.timer = max(0, self.timer + 1)
        if self.timer < Player.SLIDE_BUFFER:
            if (
                self.owner.slide_input_timer
                and self.owner.state_machine.previous_state.id == States.AIR
            ):
                self.switch(States.SLIDE)
        
        # switch states
        if self.owner.velocity.x == 0:
            self.switch(States.IDLE)
        
        if not self.owner.on_ground:
            self.switch(States.AIR)
        