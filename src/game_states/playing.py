from src.util import State
from src.camera import CAMERA
from .game_states import GameStates


class Playing(State):
    def __init__(self):
        super().__init__(GameStates.PLAYING)

    def on_enter(self):
        CAMERA.boundary = self.owner.level.tilemap.rect

    def update(self):
        self.owner.level.update()
        CAMERA.set_render_callback(self.owner.level.render) 
        CAMERA.move_to(self.owner.level.player.center)
