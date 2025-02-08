import asyncio
import sys
import pygame
from src.util import Assets, CommandPrompt, Vec2
from .debug import Debug
from .clock import Clock
from .level import Level
from .camera import Camera
from .stars import StarSpawner

WINDOW_SCALE = 4
DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180
ASPECT_RATIO = DISPLAY_WIDTH / DISPLAY_HEIGHT

class Game:
    def __init__(self):
        pygame.init()

        self.running = False
        self.paused = False
        self.command_prompt = CommandPrompt()

        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * WINDOW_SCALE, DISPLAY_HEIGHT * WINDOW_SCALE),
            pygame.SCALED
        )
        self.camera = Camera(Vec2(DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.fullscreen = False
        Assets.load_assets()

        pygame.display.set_caption('Astro')
        pygame.display.set_icon(Assets.ICON)

        self.level = None
        self.new_level()
    
    async def run(self):
        self.running = True
       
        while self.running:
            Debug.update()
            Debug.add_display(f'fps: {Clock.fps()}')
            Debug.add_display(self.level.player.debug)

            for event in pygame.event.get():
                self.handle_event(event)
                self.command_prompt.handle_event(event)
            
            self.handle_commands()

            if not self.command_prompt.enabled and not self.paused:
                self.camera.update()
                self.camera.move_to(self.level.player.center)
                self.level.star_spawner.update()
                for entity in self.level.entities:
                    entity.update()

            # draw command prompt
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
        self.camera.set_level(self.level)

        star_spawner = StarSpawner()
        star_spawner.spawn(50)
        self.level.star_spawner = star_spawner
        print(self.level.entities)

    def handle_commands(self):
        command = self.command_prompt.pop_command()
        if command == '': 
            return

        player = self.level.player
        match command.split():
            case ['g']:
                player.toggle_ghost()
            case ['d']:
                Debug.toggle()
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
            case ['f']:
                self.toggle_fullscreen()
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
        self.fullscreen = not self.fullscreen

        if self.fullscreen:
            size = (0, 0)
            mode = pygame.FULLSCREEN
        else:
            size = (DISPLAY_WIDTH * WINDOW_SCALE, DISPLAY_HEIGHT * WINDOW_SCALE)
            mode = pygame.RESIZABLE

        self.window = pygame.display.set_mode(size, mode)
    