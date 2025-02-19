from random import randint, choice
import pygame
from src.util import Assets, State, Vec2
from src.game.menu import Menu, Button, ToggleButton, SliderButton, InputButton
from src.game.entities import StarSpawner
import src.game.settings as settings
import src.game.inputs as inputs
from .game_states import GameStates

class MainMenu(State):
    def __init__(self):
        super().__init__(GameStates.MAIN_MENU)
        self.background_color = (24, 20, 37)
        self.star_spawner = StarSpawner(invert_depth=True)
        self.camera_movement: pygame.Vector2 = None

        self.menu = Menu(
            pages = [
                [
                    Button('Play', self._play),
                    Button('Settings', self._switch_to_settings), 
                    Button('Quit', self._quit)
                ],
                [
                    ToggleButton('Fullscreen', key='fullscreen', callback=lambda x: self.owner.set_fullscreen(x)),
                    SliderButton('Fuel UI Alpha', key='fuel_ui_alpha'),
                    Button('Audio', self._switch_to_audio),
                    Button('Controls', self._switch_to_controls),
                    Button('Reset Defaults', self._reset_defaults),
                    Button('Back', self._switch_to_main)
                ],
                [
                    SliderButton('Master Volume', key='master_volume', callback=self._update_volume),
                    SliderButton('Sfx Volume', key='sfx_volume', callback=self._update_volume),
                    SliderButton('Music Volume', key='music_volume', callback=self._update_volume),
                    Button('Back', self._switch_to_settings)
                ],
                [
                    InputButton('Up', key='up', callback=lambda x: self._set_movement(x)),
                    InputButton('Down', key='down', callback=lambda x: self._set_movement(x)), 
                    InputButton('Left', key='left', callback=lambda x: self._set_movement(x)),
                    InputButton('Right', key='right', callback=lambda x: self._set_movement(x)),
                    InputButton('Jump', key='jump', callback=lambda x: self._set_movement(x)),
                    Button('Back', self._switch_to_settings)
                ]
            ],
            position=Vec2(16, 180 - 16),
        )
    
    def on_enter(self):
        self.star_spawner.spawn(30)
        self.owner.camera.boundary = None
        self.camera_movement = pygame.Vector2(
            choice([-1, 1]) * randint(20, 30), 
            choice([-1, 1]) * randint(5, 15)
        )
    
    def on_exit(self):
        self.star_spawner.clear()

    def update(self):
        self.owner.camera.set_render_callback(self.render)
        self.owner.camera.move_to(self.owner.camera.pos + self.camera_movement)
        self.menu.update()
    
    def render(self, display, offset):
        display.fill(self.background_color)
        self.star_spawner.render(display, offset)
        self.menu.render(display, offset)

    def _switch_to_main(self):
        self.menu.change_page(0)

    def _switch_to_settings(self):
        self.menu.change_page(1)
    
    def _switch_to_audio(self):
        self.menu.change_page(2)
    
    def _switch_to_controls(self):
        self.menu.change_page(3)
    
    def _reset_defaults(self):
        if not settings.get('fullscreen'):
            self.owner.set_fullscreen(True)
        settings.reset_defaults()
        settings.save()
        inputs.reset_defaults()
        inputs.save()
        Assets.SOUNDS.update_sounds()
    
    def _update_volume(self):
        settings.save()
        Assets.SOUNDS.update_sounds()
    
    def _play(self):
        self.owner.state_machine.switch(GameStates.PLAYING)
    
    def _quit(self):
        self.owner.running = False

    def _set_movement(self, value: int):
        self.menu.movement_enabled = value
