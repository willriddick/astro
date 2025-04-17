import random
from src.util import State, Vec2 
from src.menu import Menu, Page, Button, TextButton
from src.level_manager import LEVEL_MANAGER
from src.camera import CAMERA
from src.networking import MsgType
from src.constants import DISPLAY_HEIGHT
import src.graphics as graphics
from .game_states import GameStates
from .lobby_helpers import render_clients, draw_wave_lines


class LobbyHost(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_HOST)
        self.background_color = graphics.PALETTE[15]

        self.JOIN_CODE_POS = Vec2(16, 16)
        self.seed = ''

        self.menu = Menu(
            position=Vec2(16, DISPLAY_HEIGHT - 16),
            pages = [
                Page([
                    TextButton('Seed', self._set_seed),
                    Button('Play', self._play),
                    Button('Cancel', self._cancel)
                ])
            ]
        )
    
    def update(self):
        CAMERA.set_render_callback(self.render)
        self.menu.update()
    
    def render(self, display, offset):
        display.fill(self.background_color)
        draw_wave_lines(display)
        self.menu.render(display, offset)

        # render join code
        node = self.owner.network_node
        if node:
            text = f'JOIN CODE: {node.join_code}'
            display.blit(
                graphics.FONT.render(text, antialias=False, color=Button.DEFAULT_COLOR), 
                self.JOIN_CODE_POS
            ) 

        render_clients(display, node)
    
    def _play(self):
        CAMERA.transition(500, focus=0, fade=-1)

        if self.seed == '':
            self.seed = random.random()

        self.owner.network_node.broadcast_message(
            MsgType.NEW_LEVEL,
            (self.seed, 0)
        )

        LEVEL_MANAGER.new_level(self.seed, 0)

        self.owner.state_machine.switch(GameStates.MULTIPLAYER)
    
    def _set_seed(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.seed = value
    
    def _cancel(self):
        CAMERA.transition(500, focus=0, fade=-1)
        self.owner.network_node.disconnect()
        self.owner.network_node.close()
        self.owner.network_node = None
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
