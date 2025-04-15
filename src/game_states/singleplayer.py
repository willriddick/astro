import pygame
import random
from src.util import State, Timer
from src.camera import CAMERA
from src.level_manager import LEVEL_MANAGER
from src.ui import UI
from .game_states import GameStates


TRANSITION_DURATION = 1000


class Singleplayer(State):
    def __init__(self):
        super().__init__(GameStates.SINGLEPLAYER)
        self.level_index = 1
        self.next_timer = Timer(TRANSITION_DURATION)
        self.next = False
        self.config_index = 0

        self.duration = 0.0
        self.fuel_cells_collected = 0

        self.ui = UI()

    def on_enter(self):
        #LEVEL_MANAGER.new_level(map_path='assets/maps/test/0.json')
        LEVEL_MANAGER.new_level(
            seed=random.random(),
            config_index=self.config_index
        )

    def update(self):
        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(self.render) 
        CAMERA.move_to(LEVEL_MANAGER.player.center)

        self.manage_rocket()
        self.ui.update(
            self.fuel_cells_collected, 
            len(LEVEL_MANAGER.current.fuel_cells),
            self.level_index
        )

        if self.next_timer.is_done and self.next:
            LEVEL_MANAGER.new_level(
                seed=random.random(),
                config_index=self.config_index
            )
            self.next = False
            self.level_index += 1

        if LEVEL_MANAGER.current.rocket.collected and not self.next:
            self.next = True
            self.next_timer.start()

            LEVEL_MANAGER.player.visible = False
            LEVEL_MANAGER.player.pause(TRANSITION_DURATION)
            CAMERA.transition(TRANSITION_DURATION * 2, 0)
        
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        LEVEL_MANAGER.current.render(display, offset)
        self.ui.render(display, offset)
   
    def manage_rocket(self):
        enable = True
        collected = 0

        for cell in LEVEL_MANAGER.current.fuel_cells:
            if not cell.collected:
                enable = False
            else: 
                collected += 1
                
        rocket = LEVEL_MANAGER.current.rocket
        if enable and not rocket.enabled:
            rocket.enable()
        
        self.fuel_cells_collected = collected 