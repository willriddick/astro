from random import randint, choice
import pygame
from src.util import State, Vec2
from src.menu import Menu, Page, Button, TextButton
from src.entities import StarSpawner
from src.camera import CAMERA
from src.networking import Host
from .game_states import GameStates


class LobbyHost(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_HOST)
        self.username = ''
        self.background_color = (24, 20, 37)
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None

        self.menu = Menu(
            position=Vec2(16, 180 - 16),
            pages = [
                Page([
                    TextButton('Username', callback=lambda x, y: self._set_username(x, y)),
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
    
    def _set_username(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.username = value
    
    def _start(self):
        self.owner.network_node = Host(self.username, port=56789)
        self.owner.network_node.start()

    def _cancel(self):
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
