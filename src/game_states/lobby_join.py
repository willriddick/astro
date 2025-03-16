from random import randint, choice
import pygame
from src.util import State, Vec2
from src.menu import Menu, Page, Button, TextButton
from src.entities import StarSpawner
from src.camera import CAMERA
from src.networking import Client
from .game_states import GameStates


class LobbyJoin(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_JOIN)
        self.username = ''
        self.background_color = (24, 20, 37)
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None

        self.menu = Menu(
            position=Vec2(16, 180 - 16),
            pages = [
                Page([
                    TextButton('Username', self._cancel),
                    TextButton('Join Code', self._cancel),
                    Button('Cancel', self._cancel)
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
    
    def _join(self):
        self.owner.network_node = Client(self.username)
        self.owner.network_node.start()
    
    def _cancel(self):
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
