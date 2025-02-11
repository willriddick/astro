from src.util import State
from .game_states import GameStates

class Playing(State):
    def __init__(self):
        super().__init__(GameStates.PLAYING)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def update(self):
        self.owner.handle_commands()
        self.owner.level.update()
        self.owner.camera.move_to(self.owner.level.player.center)
        self.owner.camera.update()
