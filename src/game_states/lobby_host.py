import random
import pygame
from src.util import State, Vec2
from src.menu import Menu, Page, Button, TextButton
from src.entities import StarSpawner
from src.camera import CAMERA
from src.clock import CLOCK
from src.level_manager import LEVEL_MANAGER
from src.networking import Host, MsgType
from .game_states import GameStates


class LobbyHost(State):
    def __init__(self):
        super().__init__(GameStates.LOBBY_HOST)
        self.username = ''
        self.background_color = (24, 20, 37)
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None

        self.start_button = Button('Start', self._start)
        self.start_button.disabled = True

        self.menu = Menu(
            position=Vec2(16, 180 - 16),
            pages = [
                Page([
                    TextButton('Username', callback=lambda x, y: self._set_username(x, y)),
                    self.start_button,
                    Button('Play', self._play),
                    Button('Canel', self._cancel)
                ]),
            ],
        )
    
    def on_enter(self):
        self.star_spawner.spawn(30)
        CAMERA.boundary = None
        self.camera_movement = pygame.Vector2(
            random.choice([-1, 1]) * random.randint(250, 1000),
            random.choice([-1, 1]) * random.randint(250, 1000)
        )
    
    def on_exit(self):
        self.star_spawner.clear()

    def update(self):
        CAMERA.set_render_callback(self.render)
        CAMERA.move_to(CAMERA.pos + self.camera_movement * CLOCK.dt)
        self.menu.update()
    
    def render(self, display, offset):
        display.fill(self.background_color)
        self.star_spawner.render(display, offset)
        self.menu.render(display, offset)
    
    def _set_username(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.username = value
        self.start_button.disabled = self.username == ''
    
    def _start(self):
        self.owner.network_node = Host(self.username, port=45678)
        self.owner.network_node.start()
        self.owner.network_node.start_session()
        print(self.owner.network_node.join_code)
    
    def _play(self):
        seed = round(random.random())
        config_index = 0
        LEVEL_MANAGER.new_level(seed, config_index)

        self.owner.state_machine.switch(GameStates.MULTIPLAYER)

        self.owner.network_node.broadcast_message(
            MsgType.NEW_LEVEL,
            (seed, config_index)
        )

    def _cancel(self):
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
