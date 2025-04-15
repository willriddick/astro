import random
import pygame
from src.util import State, Vec2
from src.menu import Menu, Page, Button, ToggleButton, SliderButton, InputButton, TextButton
from src.entities import StarSpawner
from src.constants import DISPLAY_HEIGHT
from src.camera import CAMERA
from src.settings import SETTINGS
from src.inputs import INPUTS
from src.sounds import SOUNDS
from src.networking import Host, Client
import src.graphics as graphics
from .game_states import GameStates


class MainMenu(State):
    def __init__(self):
        super().__init__(GameStates.MAIN_MENU)
        self.background_color = graphics.PALETTE[15]
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None

        # settings
        self.resolution_slider = SliderButton(
            'Resolution', 
            key='window_scale', 
            min_value=1, max_value=7,
            callback=lambda _: self.owner.set_fullscreen(SETTINGS.get('fullscreen'))
        )
        self.resolution_slider.disabled = SETTINGS.get('fullscreen')

        # multiplayer 
        self.username = ''
        self.join_code = ''
        self.join_button = Button('Join', self._join)
        self.join_button.disabled = True
        self.start_button = Button('Start', self._start)
        self.start_button.disabled = True

        # create pages
        self.menu = Menu(
            position=Vec2(16, DISPLAY_HEIGHT - 16),
            pages = [
                Page([
                    Button('Play', self._switch_to_play),
                    Button('Settings', self._switch_to_settings), 
                    Button('Quit', self._quit)
                ], default_index=0, reset_index=True),
                Page([
                    Button('Display', self._switch_to_display),
                    Button('Audio', self._switch_to_audio),
                    Button('Controls', self._switch_to_controls),
                    Button('Reset Defaults', self._reset_defaults),
                    Button('Back', self._switch_to_main)
                ]),
                Page([
                    ToggleButton('Show FPS', key='show_fps', callback=lambda _: SETTINGS.save()),
                    ToggleButton('Show Gamertag', key='show_gamertag', callback=lambda _: SETTINGS.save()),
                    ToggleButton('Fullscreen', key='fullscreen', callback=lambda x: self._set_fullscreen(x)),
                    self.resolution_slider,
                    SliderButton('UI Alpha', key='ui_alpha'),
                    SliderButton('Fuel UI Alpha', key='fuel_ui_alpha'),
                    Button('Back', self._switch_to_settings)
                ], default_index=6),
                Page([
                    SliderButton('Master Volume', key='master_volume', callback=self._update_volume),
                    SliderButton('Sfx Volume', key='sfx_volume', callback=self._update_volume),
                    SliderButton('Music Volume', key='music_volume', callback=self._update_volume),
                    Button('Back', self._switch_to_settings)
                ], default_index=3),
                Page([
                    InputButton('Up', key='up', callback=lambda x: self._set_movement(x)),
                    InputButton('Down', key='down', callback=lambda x: self._set_movement(x)), 
                    InputButton('Left', key='left', callback=lambda x: self._set_movement(x)),
                    InputButton('Right', key='right', callback=lambda x: self._set_movement(x)),
                    InputButton('Jump', key='jump', callback=lambda x: self._set_movement(x)),
                    Button('Back', self._switch_to_settings)
                ], default_index=5),
                Page([
                    Button('Singleplayer', self._start_singleplayer),
                    Button('Host', self._switch_to_host),
                    Button('Join', self._switch_to_join),
                    Button('Back', self._switch_to_main), 
                ]),
                Page([
                    TextButton('Username', callback=lambda x, y: self._set_host_username(x, y)),
                    self.start_button,
                    Button('Canel', self._switch_to_play)
                ], default_index=2),
                Page([
                    TextButton('Username', callback=lambda x, y: self._set_join_username(x, y)),
                    TextButton('Join Code', callback=lambda x, y: self._set_join_code(x, y)),
                    self.join_button,
                    Button('Cancel', self._switch_to_play)
                ], default_index=3)
            ],
        )
    
    def on_enter(self):
        self.star_spawner.spawn(30)
        CAMERA.boundary = None
        self.camera_movement = pygame.Vector2(
            random.choice([-1, 1]) * random.randint(5, 30),
            random.choice([-1, 1]) * random.randint(5, 30)
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

    def _switch_to_main(self):
        self.menu.change_page(0)
        SETTINGS.save()

    def _switch_to_settings(self):
        self.menu.change_page(1)
    
    def _switch_to_display(self):
        self.menu.change_page(2)
    
    def _switch_to_audio(self):
        self.menu.change_page(3)
    
    def _switch_to_controls(self):
        self.menu.change_page(4)

    def _switch_to_play(self):
        self.owner.network_node = None
        self.menu.change_page(5)
    
    def _switch_to_host(self):
        self.menu.change_page(6)
    
    def _switch_to_join(self):
        self.menu.change_page(7)
    
    def _start_singleplayer(self):
        self.owner.state_machine.switch(GameStates.SINGLEPLAYER)
        CAMERA.transition(1000, focus=1, fade=-1)
    
    def _start_multiplayer(self):
        self.owner.state_machine.switch(GameStates.MULTIPLAYER)
    
    def _join_session(self):
        self.owner.state_machine.switch(GameStates.LOBBY_JOIN)
    
    def _host_session(self):
        self.owner.state_machine.switch(GameStates.LOBBY_HOST)
    
    def _set_join_username(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.username = value
        self.join_button.disabled = self.username == '' or self.join_code == ''
    
    def _set_join_code(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.join_code = value
        self.join_button.disabled = self.username == '' or self.join_code == ''
    
    def _set_host_username(self, selected: bool, value: str):
        self.menu.movement_enabled = not selected 
        self.username = value
        self.start_button.disabled = self.username == ''
    
    async def _join(self):
        self.owner.network_node = Client(self.username)
        self.owner.network_node.start()
        joined = await self.owner.network_node.join(self.join_code.upper())

        if joined:
            self.owner.state_machine.switch(GameStates.LOBBY_JOIN)
        else:
            print('Failed to join session')

    def _start(self):
        self.owner.network_node = Host(self.username, port=45678)
        self.owner.network_node.start()
        self.owner.network_node.start_session()
        self.owner.state_machine.switch(GameStates.LOBBY_HOST)
    
    def _reset_defaults(self):
        if not SETTINGS.get('fullscreen'):
            self.owner.set_fullscreen(True)
        SETTINGS.reset_defaults()
        SETTINGS.save()
        INPUTS.reset_defaults()
        INPUTS.save()
        SOUNDS.update_sounds()
    
    def _set_fullscreen(self, value: bool):
        self.owner.set_fullscreen(value)
        self.resolution_slider.disabled = value
    
    def _update_volume(self, _):
        SETTINGS.save()
        SOUNDS.update_sounds()

    def _quit(self):
        self.owner.running = False

    def _set_movement(self, value: int):
        self.menu.movement_enabled = value
