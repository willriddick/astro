import pygame
from src.util import State, Timer
from src.camera import CAMERA
from src.clock import CLOCK
from src.level_manager import LEVEL_MANAGER
from src.level_gen import CONFIGS
from src.ui import UserInterface
from .game_states import GameStates


TRANSITION_DURATION = 1000


class Singleplayer(State):
    def __init__(self):
        super().__init__(GameStates.SINGLEPLAYER)
        self.level_index = 1
        self.next_timer = Timer(TRANSITION_DURATION)
        self.next = False

        self.duration = 0.0
        self.fuel_cells_collected = 0

        self.ui = UserInterface(LEVEL_MANAGER.palette_index)
        self.ui.reset()

    def on_enter(self):
        CAMERA.transition(1000, focus=1, fade=-1)
        self.level_index = 1
        self.duration = 0.0
        self.fuel_cells_collected = 0
        self.ui.palette_index = LEVEL_MANAGER.palette_index
        self.ui.reset()

    def update(self):
        self.duration += CLOCK.dt

        LEVEL_MANAGER.current.update()
        CAMERA.set_render_callback(self.render) 
        CAMERA.move_to(LEVEL_MANAGER.player.center)

        self.fuel_cells_collected = manage_rocket()

        self.ui.update(
            self.duration,
            self.fuel_cells_collected, 
            len(LEVEL_MANAGER.current.fuel_cells),
            self.level_index
        )

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
                # create a new level
                self.level_index += 1
                LEVEL_MANAGER.new_level(config_index=self.level_index - 1)
                self.next = False
            else:
                # return to main menu
                self.owner.state_machine.switch(GameStates.MAIN_MENU)
                self.next = False
        
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        LEVEL_MANAGER.current.render(display, offset)
        self.ui.render(display, offset)
    

def manage_rocket() -> int:
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
