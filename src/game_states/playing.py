from src.util import State
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from .game_states import GameStates


class Playing(State):
    def __init__(self):
        super().__init__(GameStates.PLAYING)

    def on_enter(self):
        LEVEL_MANAGER.new_level()

    def update(self):
        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(LEVEL_MANAGER.current.render) 
        CAMERA.move_to(LEVEL_MANAGER.player.center)
