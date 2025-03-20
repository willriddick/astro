import random
from src.util import State, Vec2 
from src.menu import Menu, Page, Button 
from src.level_manager import LEVEL_MANAGER
from src.camera import CAMERA
from src.networking import MsgType
import src.graphics as graphics
from .game_states import GameStates


class LobbyHost(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_HOST)
        self.background_color = graphics.PALETTE[15]

        self.JOIN_CODE_POS = Vec2(16, 16)

        self.menu = Menu(
            position=Vec2(16, 180 - 16),
            pages = [
                Page([
                    Button('Play', self._play),
                    Button('Leave', self._leave)
                ])
            ]
        )
    
    def update(self):
        CAMERA.set_render_callback(self.render)
        self.menu.update()
    
    def render(self, display, offset):
        display.fill(self.background_color)
        self.menu.render(display, offset)

        # render join code
        if self.owner.network_node:
            text = self.owner.network_node.join_code
            display.blit(
                graphics.FONT.render(text, antialias=False, color=Button.DEFAULT_COLOR), 
                self.JOIN_CODE_POS
            ) 
    
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
