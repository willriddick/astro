from src.util import State
from .states import PlayerState

class StateAir(State):
    def __init__(self):
        super().__init__('air', PlayerState.AIR)
    
    def update(self):
        self.owner.handle_movement(self.owner.air_move_speed, self.owner.air_acc)
        self.owner.handle_gravity()
        
        if self.owner.velocity.y > 0:
            self.owner.sprite.set_animation('air_down')
        else:
            self.owner.sprite.set_animation('air_up')

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
    