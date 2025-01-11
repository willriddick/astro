from random import choice
from src.util import State
from ..player import Player, PlayerState, Animation

class Run(State):
    def __init__(self):
        super().__init__(PlayerState.RUN)

    def on_enter(self):
        self.timer = 0
        
    def update(self):
        self.owner.accelerate_x(self.owner.move_dir.x, Player.GROUND_MOVE_SPEED, Player.GROUND_ACC)
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.handle_jump()
        self.handle_animation()

        self.timer = max(0, self.timer + 1)
        if self.timer < 5:
            if (
                self.owner.slide_input_timer
                and self.owner.state_machine.previous_state.id == PlayerState.AIR
            ):
                self.switch(PlayerState.SLIDE)
        
        if self.owner.velocity.x == 0:
            self.switch(PlayerState.IDLE)
        
        if not self.owner.on_ground:
            self.switch(PlayerState.AIR)
        
    def handle_animation(self):
        move_dir = self.owner.move_dir.x
        if move_dir != 0 and move_dir != self.owner.last_facing_dir:
            self.owner.rotate_dir = choice(Player.ROTATE_CHOICE)
            self.owner.sprite.animate(Animation.FRONT, Player.ROTATE_DURATION)
        
        if move_dir != 0:
            self.owner.sprite.flip = move_dir == -1
            self.owner.last_facing_dir = move_dir
        
        self.owner.sprite.queue_animation(Animation.RUN)
