import sys
import threading
import pygame
from src.tilemap import Tilemap, TileType
from src.util import load_sprite_sheet
from .player import Player

FPS = 60
WINDOW_SCALE = 3
DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180
ASPECT_RATIO = DISPLAY_WIDTH / DISPLAY_HEIGHT

class Game:
    def __init__(self):
        pygame.init()

        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * WINDOW_SCALE, DISPLAY_HEIGHT * WINDOW_SCALE),
            pygame.RESIZABLE)
        self.fullscreen = False

        self.FONT = pygame.font.Font('assets/fonts/DePixelIllegible.ttf', 8)
        
        self.TYPES = {
            TileType('stone', 
                load_sprite_sheet('stone_tileset/stone_tileset.png', (16,16)), 
                autotile=True, 
                tile_size=16
            ),
        }
        self.tilemap: Tilemap = None

        pygame.display.set_caption('GAME')

        self.clock = pygame.time.Clock()
        
        self.camera_offset = (0, 0)

        self.p1 = Player((self.display.get_width() // 2, self.display.get_height() // 2))
        self.players = pygame.sprite.Group()
        self.players.add(self.p1)

        self.running = False
        self.command_thread = threading.Thread(target=self.handle_commands)
        self.command_thread.daemon = True
    
    def run(self):
        self.running = True
        self.command_thread.start()
        self.handle_game()

    def handle_game(self):
        self.tilemap = Tilemap.load('maps/test1', self.TYPES)

        while self.running:
            self.display.fill((0, 0, 0, 0))
            for event in pygame.event.get():
                self.handle_event(event)
            
            self.tilemap.render(self.display, self.camera_offset)
            for player in self.players:
                player.update(self.tilemap)
                player.render(self.display, self.camera_offset)
            
            text = f'{self.p1.state_machine.current_state.name}\n'
            text += f'{self.p1.velocity}\n'
            text += '\n'.join(f'{dir_.name}: {val}' for dir_, val in self.p1.collisions.items())
            text_surf = self.FONT.render(text, antialias=False, color=(255, 255, 255))
            self.display.blit(text_surf, (0, 0))

            try:
                self.window.blit(pygame.transform.scale(self.display, self.window.get_size()))
                pygame.display.update()
                self.clock.tick(FPS) 
            except:
                self.running = False

        pygame.quit()
        sys.exit()

    def handle_commands(self):
        while self.running:
            try:
                command = input()
                match command.split():
                    case ['/help']:
                        print('Available commands:')
                        print('/help - Show this help message')
                        print('/load - Load new tilemap')
                        print('/quit - Quit the game')
                    case ['/load', path]:
                        self.tilemap = Tilemap.load(path, self.TYPES)
                    case ['/quit']:
                        self.running = False
                    case _:
                        print(f'Unknown command: {command}')
                        print('Type /help for a list of commands')
            except EOFError:
                self.running = False
            except KeyboardInterrupt:
                self.running = False
    
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
    