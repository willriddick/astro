import sys
import os
import threading
import pygame
import random
from src.tilemap import Tilemap, TileType
from src.util import load_sprite_sheet, load_image
from src.level_gen import LevelBuilder, Level, Display, Attribute
from .player import Player
from .camera import Camera

FPS = 60
WINDOW_SCALE = 3
DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180
ASPECT_RATIO = DISPLAY_WIDTH / DISPLAY_HEIGHT

class Game:
    def __init__(self):
        pygame.init()

        self.camera = Camera(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * WINDOW_SCALE, DISPLAY_HEIGHT * WINDOW_SCALE),
            pygame.RESIZABLE)
        self.fullscreen = False
        pygame.display.set_caption('GAME')

        self.FONT = pygame.font.Font('assets/fonts/DePixelIllegible.ttf', 8)
        
        self.TYPES = {
            TileType('stone', 
                load_sprite_sheet(load_image('tileset/rock.png'), (16,16)), 
                autotile=True, 
                tile_size=16
            ),
        }
        self.tilemap = Tilemap(self.TYPES, tile_size=16)

        config = 'src/level_gen/configs/test1.json'
        self.level: Level = LevelBuilder.generate_level(config)
        print(Display(self.level))

        spawn_pos = (0, 0)

        for room in self.level.map.values():
            map_folder = f'maps/{room.key}' 
            map_paths: list[str] = []
            for name in os.listdir(map_folder):
                map_paths.append(map_folder + '/' + name)
            map_path = random.choice(map_paths)
            new_map = Tilemap.load(map_path, self.TYPES)
            self.tilemap.place(new_map, room.position, False)
            if room.has_attribute(Attribute.ENTRANCE):
                spawn_pos = (room.position.x * 10 * self.tilemap.tile_size, room.position.y * 8 * self.tilemap.tile_size)

        self.p1 = Player(spawn_pos)
        self.players = list[Player]

        self.clock = pygame.time.Clock()
        self.running = False
        self.command_thread = threading.Thread(target=self.handle_commands)
        self.command_thread.daemon = True
    
    def run(self):
        self.running = True
        self.command_thread.start()
        self.handle_game()

    def handle_game(self):
        self.camera.tilemap = self.tilemap
        self.camera.set_boundary(self.tilemap.get_rect())
        self.camera.add(self.p1)

        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            
            self.p1.update(self.tilemap)
            self.camera.move_to(self.p1.get_center())
            self.camera.update()
            
            text = f'{self.p1.state_machine.current_state.name}\n'
            text += f'{int(self.p1.pos.x):04},{int(self.p1.pos.y):04} \n'
            text += '\n'.join(f'{dir_.name}: {val}' for dir_, val in self.p1.collisions.items())
            text_surf = self.FONT.render(text, antialias=False, color=(255, 255, 255))
            self.camera.display.blit(text_surf, (0, 0))

            try:
                self.window.blit(pygame.transform.scale(self.camera.display, self.window.get_size()))
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
    