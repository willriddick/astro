from src.util import State
from src.util import State, Vec2 
from src.menu import Menu, Page, Button 
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from src.networking import MsgType
import src.graphics as graphics
from .game_states import GameStates


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

        if self.owner.network_node:
            events = self.owner.network_node.get_events()
            for event in events:
                if event.type == MsgType.NEW_LEVEL:
                    seed, config_index = event.data
                    print(f'recieved NEW_LEVEL message: {seed} {config_index}')
                    LEVEL_MANAGER.new_level(seed, config_index)
                    self.owner.state_machine.switch(GameStates.MULTIPLAYER)
    
    def render(self, display, offset):
        display.fill(self.background_color)
        self.menu.render(display, offset)
    
    def _leave(self):
        self.owner.network_node.disconnect()
        self.owner.network_node.close()
        self.owner.network_node = None
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
