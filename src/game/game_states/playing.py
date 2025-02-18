from src.util import State
from .game_states import GameStates

class Playing(State):
    def __init__(self):
        super().__init__(GameStates.PLAYING)

    def on_enter(self):
        self.owner.camera.boundary = self.owner.level.tilemap.rect

    def update(self):
        self.owner.level.update()
        self.owner.camera.set_render_callback(self.owner.level.render) 
        self.owner.camera.move_to(self.owner.level.player.center)
