import random
from src.util import State, Vec2 
from src.menu import Menu, Page, Button 
from src.level_manager import LEVEL_MANAGER
from src.camera import CAMERA
from src.networking import MsgType
from .game_states import GameStates


class LobbyHost(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_HOST)
        self.background_color = (24, 20, 37)

        self.menu = Menu(
            position=Vec2(16, 180 - 16),
            pages = [
                Page([
                    Button('Play', self._play),
                    Button('Leave', self._leave)
                ])
            ]
        )
    
    def on_enter(self):
        print(self.owner.network_node.username)
        print(self.owner.network_node.join_code)

    def update(self):
        CAMERA.set_render_callback(self.render)
        self.menu.update()
    
    def render(self, display, offset):
        display.fill(self.background_color)
        self.menu.render(display, offset)
    
    def _play(self):
        seed = round(random.random())
        config_index = 0
        LEVEL_MANAGER.new_level(seed, config_index)

        self.owner.state_machine.switch(GameStates.MULTIPLAYER)

        self.owner.network_node.broadcast_message(
            MsgType.NEW_LEVEL,
            (seed, config_index)
        )
    
    def _leave(self):
        self.owner.network_node.disconnect()
        self.owner.network_node.close()
        self.owner.network_node = None
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
