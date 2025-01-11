from src.util import State
from ..player import Player, PlayerState, Animation

class Idle(State):
    def __init__(self):
        super().__init__(PlayerState.IDLE)
    
    def on_enter(self):
        self.owner.sprite.set_animation_duration(Animation.IDLE_A, 30, Animation.IDLE_B)
    
    def update(self):
        self.owner.apply_gravity(Player.GRAVITY, Player.FALL_SPEED)
        self.owner.handle_jump()

        if self.owner.move_dir.x != 0:
            self.switch(PlayerState.RUN)
        
        if not self.owner.on_ground:
            self.switch(PlayerState.AIR)
    