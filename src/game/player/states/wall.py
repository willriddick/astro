from src.util import State
from .states import PlayerState

class StateWall(State):
    def __init__(self):
        super().__init__('wall', PlayerState.WALL)

    def on_enter(self):
        self.owner.sprite.flip = (self.owner.move_dir == 1)
        self.owner.sprite.set_animation('idle')
    
    def update(self):
        self.owner.velocity.y = min(
            self.owner.velocity.y + self.owner.wall_slide_gravity,
            self.owner.wall_slide_speed
        )

        self.owner.handle_wall_jump()

        if self.owner.on_ground:
            if self.owner.velocity.x == 0:
                self.switch(PlayerState.IDLE)
            else:
                self.switch(PlayerState.RUN)
        
        if not self.owner.slide_left and not self.owner.slide_right:
            self.switch(PlayerState.AIR)
    
   