import random
import pygame
from src.util import State, Vec2 
from src.menu import Menu, Page, Button, TextButton 
from src.level_manager import LEVEL_MANAGER
from src.camera import CAMERA
from src.sounds import SOUNDS
from src.constants import DISPLAY_HEIGHT
from src.inputs import INPUTS
import src.graphics as graphics
from .game_states import GameStates
from .lobby_helpers import draw_wave_lines, draw_player_card


TRANSITION_DURATION = 500


class LobbySingleplayer(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_SINGLEPLAYER)
        self.background_color = graphics.PALETTE[15]

        self.seed = ''
        self.palette_index = random.randint(0, len(graphics.PLAYER_PALETTES) - 1)

        self.menu = Menu(
            position=Vec2(16, DISPLAY_HEIGHT - 16),
            pages = [
                Page([
                    TextButton('Seed', self._set_seed),
                    Button('Play', self._play),
                    Button('Cancel', self._cancel)
                ], default_index=0, reset_index=True)
            ]
        )
    
    def on_enter(self):
        CAMERA.offset = pygame.Vector2(0, 0)
        self.seed = ''
    
    def update(self):
        CAMERA.set_render_callback(self.render)
        self.menu.update()

        pal_dir = INPUTS.get_dir(just_pressed=True).x
        if pal_dir:
            self._set_palette(pal_dir)
    
    def render(self, display, offset):
        display.fill(self.background_color)
        draw_wave_lines(display)
        draw_player_card(display, '', self.palette_index, TextButton.DEFAULT_COLOR, Vec2(32, 64))
        self.menu.render(display, offset)

    def _set_seed(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.seed = value
    
    def _set_palette(self, value: int):
        self.palette_index = (self.palette_index + value) % len(graphics.PLAYER_PALETTES)
        SOUNDS.play('blip')
    
    def _play(self):
        if self.seed == '':
            self.seed = random.random()
        CAMERA.transition(TRANSITION_DURATION, focus=0, fade=-1)  # fade the screen
        LEVEL_MANAGER.palette_index = self.palette_index
        LEVEL_MANAGER.new_level(self.seed, 0)
        LEVEL_MANAGER.seed = self.seed
        self.owner.state_machine.switch(GameStates.SINGLEPLAYER)
    
    def _cancel(self):
        CAMERA.transition(500, focus=0, fade=-1)
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
 