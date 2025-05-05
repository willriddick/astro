import pygame
from src.util import State, Timer
from src.camera import CAMERA
from src.clock import CLOCK
from src.sounds import SOUNDS
from src.inputs import INPUTS
from src.level_manager import LEVEL_MANAGER
from src.level_gen import CONFIGS
from src.constants import DISPLAY_HEIGHT
from src.ui import UserInterface
from src.menu import Menu, Page, Button
from .game_states import GameStates


TRANSITION_DURATION = 1000


class Singleplayer(State):
    def __init__(self):
        super().__init__(GameStates.SINGLEPLAYER)
        self.paused = False

        self.level_index = 1
        self.next_timer = Timer(TRANSITION_DURATION)
        self.next = False

        self.duration = 0.0
        self.fuel_cells_collected = 0

        self.ui = UserInterface(LEVEL_MANAGER.palette_index)
        self.ui.reset()

        self.pause_menu = Menu(pages=[
                Page(buttons=[
                    Button('Resume', self._resume), 
                    Button('Quit', self._quit)
                ], reset_index=True)
            ], 
            position=pygame.Vector2(16, DISPLAY_HEIGHT - 16),
        )

    def on_enter(self):
        CAMERA.transition(1000, focus=1, fade=-1)
        self.level_index = 1
        self.duration = 0.0
        self.fuel_cells_collected = 0
        self.ui.palette_index = LEVEL_MANAGER.palette_index
        self.ui.reset()
        self.pause_menu.change_page(0)
        LEVEL_MANAGER.player.multiplayer = False

    def update(self):
        if INPUTS.get('escape', just_pressed=True):
            self._toggle_pause()

        if self.paused:
            self.pause_menu.update()
            return
    
        self.duration += CLOCK.dt

        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(self.render) 
        CAMERA.move_to(LEVEL_MANAGER.player.center)

        self.fuel_cells_collected = manage_fuel_cells()

        self.ui.update(
            self.duration,
            self.fuel_cells_collected, 
            len(LEVEL_MANAGER.current.fuel_cells),
            self.level_index
        )

        self.handle_rocket()

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        LEVEL_MANAGER.current.render(display, offset)
        self.ui.render(display, offset)

        if self.paused:
            overlay = pygame.Surface(display.get_size(), flags=pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            display.blit(overlay, (0, 0))
            self.pause_menu.render(display, offset)
    
    def new_level(self) -> None:
        self.level_index += 1
        LEVEL_MANAGER.new_level(config_index=self.level_index - 1)
    
    def handle_rocket(self) -> None:
        # check if rocket has been collected (make sure next is false so this only triggers once)
        if LEVEL_MANAGER.current.rocket.collected and not self.next:
            self.next = True
            self.next_timer.start()  # start the timer until next level is created
            CAMERA.transition(TRANSITION_DURATION * 2, 0)  # fade the screen

            player = LEVEL_MANAGER.player  # pause the player for rocket animation
            player.visible = False
            player.velocity = pygame.Vector2(0, 0)
            player.pause(TRANSITION_DURATION)
        
        # if next timer is done
        if self.next_timer.is_done and self.next:
            # if there are more levels to play
            if self.level_index < len(CONFIGS):
                self.new_level()
                self.next = False
            else:
                self.owner.state_machine.switch(GameStates.MAIN_MENU)
                self.next = False
   
    def _toggle_pause(self) -> None:
        SOUNDS.play('select', pitch_index=1)
        if self.paused:
            self._resume()
        else:
            self._pause()
   
    def _pause(self) -> None:
        self.paused = True
        LEVEL_MANAGER.player.pause(-1)

    def _resume(self) -> None:
        self.paused = False
        LEVEL_MANAGER.player.unpause()
    
    def _quit(self) -> None:
        self._resume()
        self.next = False
        self.next_timer.reset()
        CAMERA.transition(TRANSITION_DURATION, 0, -1)
        self.owner.state_machine.switch(GameStates.MAIN_MENU)
              

def manage_fuel_cells() -> int:
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
    
    return collected 
