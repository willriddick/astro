import asyncio
import sys
import pygame
from src.util import Assets, CommandPrompt, Vec2, StateMachine
from .game_states import GameStates
from .debug import Debug
from .clock import Clock
from .level import Level
from .camera import Camera
from .settings import Settings
from .input import Input

DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180
ASPECT_RATIO = DISPLAY_WIDTH / DISPLAY_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.input = Input()

        self.running = False
        self.paused = False

        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * self.settings.window_scale, DISPLAY_HEIGHT * self.settings.window_scale),
            pygame.SCALED
        )
        self.camera = Camera(Vec2(DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.set_fullscreen(self.settings.fullscreen)

        Assets.load()
        pygame.display.set_caption('Astro')
        pygame.display.set_icon(Assets.ICON)

        self.command_prompt = CommandPrompt()

        from .game_states import MainMenu, Playing
        self.state_machine = StateMachine(self, [MainMenu(), Playing()])

        self.level = None
        self.new_level()
    
    async def run(self):
        self.running = True
        #Assets.SOUNDS.play('track1', loops=-1)
       
        while self.running:
            Debug.update()
            Debug.add_display(f'fps: {Clock.fps()}')

            for event in pygame.event.get():
                self.handle_event(event)
                self.command_prompt.handle_event(event)

            if not self.paused:
                self.state_machine.update()
            self.camera.update()

            # handle commmands and draw command prompt
            self.handle_commands()
            self.command_prompt.render(self.camera.display)

            try:
                self.window.blit(pygame.transform.scale(self.camera.display, self.window.get_size()))
                pygame.display.flip()
                Clock.update()
            except KeyboardInterrupt:
                self.running = False
            
            await asyncio.sleep(0)

        pygame.quit()
        sys.exit()

    def new_level(self, map_path: str = None, seed: int = None):
        self.level = Level(map_path=map_path, seed=seed)
        self.level.player.camera = self.camera
        self.camera.set_pos(self.level.spawn_pos)
        print(self.level.entities)

    def handle_commands(self):
        command = self.command_prompt.pop_command()
        if command == '': 
            return

        player = self.level.player
        match command.split():
            case ['d']:
                Debug.toggle()
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
                Assets.SOUNDS.play('teleport')
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
                self.paused = not self.paused
    
    def handle_resize(self, width, height):
        new_width = width
        new_height = int(new_width / ASPECT_RATIO)
        if new_height > height:
            new_height = height
            new_width = int(new_height * ASPECT_RATIO)
        self.window = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)
    
    def toggle_fullscreen(self):
        self.set_fullscreen(not self.settings.fullscreen)

    def set_fullscreen(self, value: bool):
        self.settings.fullscreen = value

        if value:
            size = (0, 0)
            mode = pygame.FULLSCREEN
        else:
            size = (DISPLAY_WIDTH * self.settings.window_scale, DISPLAY_HEIGHT * self.settings.window_scale)
            mode = pygame.RESIZABLE

        self.window = pygame.display.set_mode(size, mode)
    