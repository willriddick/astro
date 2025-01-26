from src.util import State, Timer
from ..player import Player
from ..enums import Animations, States

class Run(State):
    def __init__(self):
        super().__init__(States.RUN)
        self.slide_timer = Timer(Player.SLIDE_BUFFER)

    def on_enter(self):
        self.slide_timer.start()
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
        if self.slide_timer.is_active:
            if (
                self.owner.slide_input_timer.is_active
                and self.owner.state_machine.previous_state.id == States.AIR
            ):
                self.switch(States.SLIDE)
        
        # switch states
        if self.owner.velocity.x == 0:
            self.switch(States.IDLE)
        
        if not self.owner.on_ground:
            self.switch(States.AIR)
        