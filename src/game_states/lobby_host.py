import random
from src.util import State, Vec2 
from src.menu import Menu, Page, Button, TextButton
from src.level_manager import LEVEL_MANAGER
from src.camera import CAMERA
from src.inputs import INPUTS
from src.sounds import SOUNDS
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
        self.palette_index = 0

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

        # swap palette
        pal_dir = INPUTS.get_dir(just_pressed=True).x
        if pal_dir:
            self._set_palette(pal_dir)

        # render join code
        node = self.owner.network_node
        if node:
            text = f'JOIN CODE: {node.join_code}'
            display.blit(
                graphics.FONT.render(text, antialias=False, color=Button.DEFAULT_COLOR), 
                self.JOIN_CODE_POS
            ) 

        render_clients(display, node, [self.palette_index, 0, 0, 0])
    
    def _play(self):
        CAMERA.transition(500, focus=0, fade=-1)

        if self.seed == '':
            self.seed = random.random()

        self.owner.network_node.broadcast_message(
            MsgType.NEW_LEVEL,
            (self.seed, 0)
        )

        LEVEL_MANAGER.palette_index = self.palette_index
        LEVEL_MANAGER.new_level(self.seed, 0)

        self.owner.state_machine.switch(GameStates.MULTIPLAYER)
    
    def _set_seed(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.seed = value
    
    def _set_palette(self, value: int):
        self.palette_index = (self.palette_index + value) % len(graphics.PLAYER_PALETTES)
        SOUNDS.play('blip')
    
    def _cancel(self):
        CAMERA.transition(500, focus=0, fade=-1)
        self.owner.network_node.disconnect()
        self.owner.network_node.close()
        self.owner.network_node = None
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
