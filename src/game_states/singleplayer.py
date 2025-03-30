import pygame
import random
from src.util import State
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from .game_states import GameStates


class Singleplayer(State):
    def __init__(self):
        super().__init__(GameStates.SINGLEPLAYER)

    def on_enter(self):
        seed = round(random.random())
        config_index = 1
        LEVEL_MANAGER.new_level(seed, config_index)
        #LEVEL_MANAGER.new_level(map_path='assets/maps/test/0.json')

    def update(self):
        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(self.render) 
        CAMERA.move_to(LEVEL_MANAGER.player.center)

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        LEVEL_MANAGER.current.render(display, offset)
   