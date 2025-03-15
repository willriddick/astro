from random import randint, choice
import pygame
from src.util import State, Vec2
from src.menu import Menu, Page, Button, ToggleButton, SliderButton, InputButton, TextButton
from src.entities import StarSpawner
from src.camera import CAMERA
from src.settings import SETTINGS
from src.inputs import INPUTS
from src.sounds import SOUNDS
from .game_states import GameStates


class MainMenu(State):
    def __init__(self):
        super().__init__(GameStates.MAIN_MENU)
        self.background_color = (24, 20, 37)
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None

        self.join_code = ''

        self.resolution_slider = SliderButton(
            'Resolution', 
            key='window_scale', 
            min_value=1, max_value=7, 
            callback=lambda _: self.owner.set_fullscreen(SETTINGS.get('fullscreen'))
        )
        self.resolution_slider.disabled = SETTINGS.get('fullscreen')

        self.menu = Menu(
            position=Vec2(16, 180 - 16),
            pages = [
                Page([
                    Button('Singleplayer', self._play_singleplayer),
                    Button('Multiplayer', self._switch_to_multiplayer),
                    Button('Settings', self._switch_to_settings), 
                    Button('Quit', self._quit)
                ]),
                Page([
                    Button('Display', self._switch_to_display),
                    Button('Audio', self._switch_to_audio),
                    Button('Controls', self._switch_to_controls),
                    Button('Reset Defaults', self._reset_defaults),
                    Button('Back', self._switch_to_main)
                ]),
                Page([
                    ToggleButton('Show FPS', key='show_fps', callback=lambda _: SETTINGS.save()),
                    ToggleButton('Fullscreen', key='fullscreen', callback=lambda x: self._set_fullscreen(x)),
                    self.resolution_slider,
                    SliderButton('Fuel UI Alpha', key='fuel_ui_alpha'),
                    Button('Back', self._switch_to_settings)
                ]),
                Page([
                    SliderButton('Master Volume', key='master_volume', callback=self._update_volume),
                    SliderButton('Sfx Volume', key='sfx_volume', callback=self._update_volume),
                    SliderButton('Music Volume', key='music_volume', callback=self._update_volume),
                    Button('Back', self._switch_to_settings)
                ]),
                Page([
                    InputButton('Up', key='up', callback=lambda x: self._set_movement(x)),
                    InputButton('Down', key='down', callback=lambda x: self._set_movement(x)), 
                    InputButton('Left', key='left', callback=lambda x: self._set_movement(x)),
                    InputButton('Right', key='right', callback=lambda x: self._set_movement(x)),
                    InputButton('Jump', key='jump', callback=lambda x: self._set_movement(x)),
                    Button('Back', self._switch_to_settings)
                ]),
                Page([
                    Button('Host', self._host_session),
                    Button('Join', self._join_session),
                    Button('Back', self._switch_to_main), 
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

    def _switch_to_multiplayer(self):
        self.menu.change_page(5)
    
    def _play_singleplayer(self):
        self.owner.state_machine.switch(GameStates.SINGLEPLAYER)
  
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
    
    def _join_session(self):
        self.owner.state_machine.switch(GameStates.LOBBY_JOIN)
    
    def _host_session(self):
        self.owner.state_machine.switch(GameStates.LOBBY_HOST)
    
    def _quit(self):
        self.owner.running = False

    def _set_movement(self, value: int):
        self.menu.movement_enabled = value
