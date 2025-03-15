from random import randint, choice
import pygame
from src.util import State, Vec2
from src.menu import Menu, Page, Button
from src.entities import StarSpawner
from src.camera import CAMERA
from .game_states import GameStates


class LobbyHost(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_HOST)
        self.background_color = (24, 20, 37)
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None

        self.menu = Menu(
            position=Vec2(16, 180 - 16),
            pages = [
                Page([
                    Button('Start', self._start),
                    Button('Canel', self._cancel)
                ]),
            ],
        )
    
    def on_enter(self):
        self.star_spawner.spawn(30)
        CAMERA.boundary = None
        self.camera_movement = pygame.Vector2(
            choice([-1, 1]) * randint(5, 30),
            choice([-1, 1]) * randint(5, 30)
        )
    
    def on_exit(self):
        self.star_spawner.clear()

    def update(self):
        CAMERA.set_render_callback(self.render)
        CAMERA.move_to(CAMERA.pos + self.camera_movement)
        self.menu.update()
    
    def render(self, display, offset):
        display.fill(self.background_color)
        self.star_spawner.render(display, offset)
        self.menu.render(display, offset)
    
    def _start(self):
        print('start')

    def _cancel(self):
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
