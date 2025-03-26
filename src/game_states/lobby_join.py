from src.util import State
from src.util import State, Vec2 
from src.menu import Menu, Page, Button 
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from src.networking import MsgType
import src.graphics as graphics
from .game_states import GameStates
from .lobby_helpers import render_clients


class LobbyJoin(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_JOIN)
        self.background_color = graphics.PALETTE[15]
    
        self.menu = Menu(
            position=Vec2(16, 180 - 16),
            pages = [
                Page([
                    Button('Leave', self._leave)
                ])
            ]
        ) 
    
    def update(self):
        CAMERA.set_render_callback(self.render)
        self.menu.update()

        node = self.owner.network_node
        if not node:
            return

        events = self.owner.network_node.get_events()
        for event in events:
            # if host starts game, switch to multiplayer state
            if event.type == MsgType.NEW_LEVEL:
                seed, config_index = event.data
                print(f'recieved NEW_LEVEL message: {seed} {config_index}')
                LEVEL_MANAGER.new_level(seed, config_index)
                self.owner.state_machine.switch(GameStates.MULTIPLAYER)

            # if host disconnects, leave game
            if event.type == MsgType.DISCONNECT:
                if event.data[0] == 0:
                    self._leave() 
    
    def render(self, display, offset):
        display.fill(self.background_color)
        self.menu.render(display, offset)

        node = self.owner.network_node
        render_clients(display, node)

    def _leave(self):
        self.owner.network_node.disconnect()
        self.owner.network_node.close()
        self.owner.network_node = None
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
