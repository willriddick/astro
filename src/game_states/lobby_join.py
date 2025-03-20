from random import randint, choice
import pygame
from src.util import State, Vec2
from src.menu import Menu, Page, Button, TextButton
from src.entities import StarSpawner
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from src.networking import Client, MsgType
from .game_states import GameStates


class LobbyJoin(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_JOIN)
        self.username = ''
        self.background_color = (24, 20, 37)
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None

        self.join_code = ''

        self.join_button = Button('Join', self._join)
        self.join_button.disabled = True

        self.menu = Menu(
            position=Vec2(16, 180 - 16),
            pages = [
                Page([
                    TextButton('Username', callback=lambda x, y: self._set_username(x, y)),
                    TextButton('Join Code', callback=lambda x, y: self._set_join_code(x, y)),
                    self.join_button,
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
        self.star_spawner.render(display, offset)
        self.menu.render(display, offset)
    
    def _update_join_button(self):
        self.join_button.disabled = self.username == '' or self.join_code == ''
    
    def _set_username(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.username = value
        self._update_join_button()
    
    def _set_join_code(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.join_code = value
        self._update_join_button()
    
    def _join(self):
        self.owner.network_node = Client(self.username)
        self.owner.network_node.start()
        self.owner.network_node.join(self.join_code.upper())
    
    def _cancel(self):
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
