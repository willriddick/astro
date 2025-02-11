from src.util import State
from .game_states import GameStates

class Menu(State):
    def __init__(self):
        super().__init__(GameStates.MENU)

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def update(self):
        self.owner.camera.update()
