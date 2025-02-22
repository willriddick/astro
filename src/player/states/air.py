from src.util import State, Timer
from src.sounds import SOUNDS
from ..player import Player
from ..enums import Animations, States

class Air(State):
    def __init__(self):
        super().__init__(States.AIR)
        self.timer = Timer(1000)
    
    def on_enter(self):
        self.timer.start()
        self.owner.sprite.set_next(Animations.AIR_UP if self.owner.velocity.y < 0 else Animations.AIR_DOWN)

    def update(self):
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.handle_jump()
        self.owner.handle_wall_jump()
        self.owner.accelerate_x(self.owner.input_dir.x, Player.AIR_MOVE_SPEED, Player.AIR_ACC)

        self.owner.handle_boost()

        # handle rotation animation
        if self.owner.rotated:
            self.owner.sprite.set_animation_duration(Animations.FRONT, Player.AIR_ROTATE_DURATION)
        self.owner.sprite.set_next(Animations.AIR_UP if self.owner.velocity.y < 0 else Animations.AIR_DOWN)
        
        if self.owner.input_dir.x != 0:
            self.owner.sprite.flip_x = self.owner.input_dir.x == -1

        # switch states
        if self.owner.wall_slide_timer.is_active:
            self.switch(States.WALL_SLIDE)

        if self.owner.on_ground:
            if self.owner.velocity.y >= 0:
                SOUNDS.play('land')

            if self.timer.is_done:
                self.owner.camera.screenshake(30, 3)

            if self.owner.velocity.x == 0:
                self.switch(States.IDLE)
            else:
                self.switch(States.RUN)
 