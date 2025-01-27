import sys
import pygame
from src.util import Assets, CommandPrompt, Vec2, draw_rect
from .clock import Clock
from .level import Level
from .camera import Camera
from .player import Player 

WINDOW_SCALE = 4
DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180
ASPECT_RATIO = DISPLAY_WIDTH / DISPLAY_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('GAME')

        self.running = False
        self.command_prompt = CommandPrompt()

        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * WINDOW_SCALE, DISPLAY_HEIGHT * WINDOW_SCALE),
            pygame.RESIZABLE
        )
        self.camera = Camera(Vec2(DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.fullscreen = False
        Assets.load_assets()

        self.level = None
        self.new('maps/10x8/1_2/test')
    
    def run(self):
        self.running = True
       
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
                self.command_prompt.handle_event(event)
            
            self.handle_commands()
            
            if not self.command_prompt.enabled:
                self.camera.update()
                self.camera.move_to(self.player.center)
                for entity in self.level.entities:
                    entity.update()

            # Draw command prompt
            self.command_prompt.render(self.camera.display)
            self.debug_display()

            try:
                self.window.blit(pygame.transform.scale(self.camera.display, self.window.get_size()))
                pygame.display.update()
                Clock.update()
            except KeyboardInterrupt:
                self.running = False

        pygame.quit()
        sys.exit()

    def new(self, map_path: str = None, seed: int = None):
        self.level = Level(map_path=map_path, seed=seed)
        self.camera.level = self.level

        self.player = Player(self.level, self.camera)
        self.player.spawn(self.level.spawn_pos)

        self.camera.boundary = self.level.tilemap.rect
        self.camera.set_pos(self.level.spawn_pos)

        self.level.entities.append(self.player)

    def debug_display(self):
        text = f'fps: {Clock.fps()}\n{self.player}'
        text_surf = Assets.FONT.render(text, antialias=False, color=(255, 255, 255))
        text_surf.set_alpha(70)
        text_rect = text_surf.get_rect()
        draw_rect(
            self.camera.display,
            rect=pygame.Rect(0, 0, 100, text_rect.height + 8),
            fill_color=(0, 0, 0, 40),
            outline_color=(0, 0, 0, 0)
        )
        self.camera.display.blit(text_surf, (4, 4))

    def handle_commands(self):
        command = self.command_prompt.pop_command()
        if command == '': 
            return

        match command.split():
            case ['g']:
                self.player.toggle_ghost()
            case ['n']:
                self.new()
            case ['n', seed]:
                self.new(seed)
            case ['p', index]:
                self.player.load_sprite(int(index))
            case ['tp', x, y]:
                self.player.pos = pygame.Vector2(int(x), int(y))
            case ['jumps', amount]:
                self.player.max_jumps = int(amount)
                self.player.jumps_remaining = self.player.max_jumps
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
            self.toggle_fullscreen()
    
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
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode(
                (DISPLAY_WIDTH * WINDOW_SCALE, DISPLAY_HEIGHT * WINDOW_SCALE), 
                pygame.RESIZABLE)
    