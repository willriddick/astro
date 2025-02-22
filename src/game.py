import asyncio
import sys
import pygame
from src.util import CommandPrompt, StateMachine
from src.constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, ASPECT_RATIO
from src.game_states import GameStates
from src.debug import DEBUG
from src.clock import CLOCK
from src.camera import CAMERA
from src.settings import SETTINGS
from src.sounds import SOUNDS
from src.level import Level
import src.assets as assets

class Game:
    def __init__(self):
        pygame.init()
        self.running = False
        self.paused = False
        scale = SETTINGS.get('window_scale')
        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * scale, DISPLAY_HEIGHT * scale),
            pygame.SCALED
        )
        self.set_fullscreen(SETTINGS.get('fullscreen'))

        assets.load()
        pygame.display.set_caption('Astro')
        pygame.display.set_icon(assets.ICON)

        self.command_prompt = CommandPrompt()

        from .game_states import MainMenu, Playing
        self.state_machine = StateMachine(self, [MainMenu(), Playing()])

        self.level = None
        self.new_level()
    
    async def run(self):
        self.running = True
        #SOUNDS.play('music/track1', loops=-1)
       
        while self.running:
            DEBUG.update()

            if SETTINGS.get('show_fps') or DEBUG.enabled:
                DEBUG.add_display(f'fps: {CLOCK.fps}')

            for event in pygame.event.get():
                self.handle_event(event)
                self.command_prompt.handle_event(event)

            if not self.paused:
                self.state_machine.update()
            CAMERA.update()

            # handle commmands and draw command prompt
            self.handle_commands()
            self.command_prompt.render(CAMERA.display)

            try:
                self.window.blit(pygame.transform.scale(CAMERA.display, self.window.get_size()))
                pygame.display.flip()
                CLOCK.update()
            except KeyboardInterrupt:
                self.running = False
            
            await asyncio.sleep(0)

        pygame.quit()
        sys.exit()

    def new_level(self, seed: int = None, map_path: str = None):
        self.level = Level(seed=seed, map_path=map_path)
        self.level.player.camera = CAMERA
        CAMERA.set_pos(self.level.spawn_pos)
        print(self.level.entities)

    def handle_commands(self):
        command = self.command_prompt.pop_command()
        if command == '': 
            return

        player = self.level.player
        match command.split():
            case ['d']:
                DEBUG.toggle()
            case ['g']:
                player.toggle_ghost()
            case ['n']:
                self.new_level()
            case ['n', seed]:
                self.new_level(seed=seed)
            case ['p', index]:
                player.load_sprite(int(index))
            case ['r']:
                player.spawn(player.spawn_position)
            case ['tp', x, y]:
                player.set_position(pygame.Vector2(int(x), int(y)))
                SOUNDS.play('teleport')
            case ['f']:
                self.toggle_fullscreen()
            case ['gs', state]:
                self.state_machine.switch(list(GameStates)[int(state)])
            case ['q']:
                self.running = False
            case _:
                print(f'Unknown command: {command}')
    
    def handle_event(self, event: pygame.Event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.VIDEORESIZE:
            self.handle_resize(event.w, event.h)
        if event.type == pygame.FULLSCREEN:
            self.toggle_fullscreen
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if event.mod & pygame.KMOD_CTRL:
                    self.paused = not self.paused
    
    def handle_resize(self, width, height):
        new_width = width
        new_height = int(new_width / ASPECT_RATIO)
        if new_height > height:
            new_height = height
            new_width = int(new_height * ASPECT_RATIO)
        self.window = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
    
    def toggle_fullscreen(self):
        self.set_fullscreen(not SETTINGS.get('fullscreen'))

    def set_fullscreen(self, value: bool):
        SETTINGS.set_key('fullscreen', value)
        if value:
            size = (0, 0)
            mode = pygame.FULLSCREEN
        else:
            scale = SETTINGS.get('window_scale')
            size = (DISPLAY_WIDTH * scale, DISPLAY_HEIGHT * scale)
            mode = pygame.RESIZABLE

        self.window = pygame.display.set_mode(size, mode)
    