import sys
import os
import threading
import pygame
import random
from src.tilemap import TileMap, Tile, TileSet
from src.level_gen import LevelBuilder, Level, Display, Attribute
from src.util import load_image, load_sprite_sheet, draw_transparent_rect
from .player import Player
from .camera import Camera

FPS = 60
WINDOW_SCALE = 3
DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180
ASPECT_RATIO = DISPLAY_WIDTH / DISPLAY_HEIGHT

class Game:
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * WINDOW_SCALE, DISPLAY_HEIGHT * WINDOW_SCALE),
            pygame.RESIZABLE)
        self.fullscreen = False
        pygame.display.set_caption('GAME')

        self.command_active = False
        self.command_input = ''

        self.FONT = pygame.font.Font('assets/fonts/DePixelIllegible.ttf', 8)
        
        self.tileset = TileSet(16)
        self.tileset.add('stone', load_sprite_sheet(load_image('tileset/rock.png'), (16,16)), True)
        self.tileset.add('door', [load_sprite_sheet(load_image('items.png'), (16,16))[0]], False)

        self.tilemap = TileMap(self.tileset, size=(0, 0), debug=False)

        self.level: Level = LevelBuilder.generate_level('configs/test1.json')
        print(Display(self.level))

        for room in self.level.map.values():
            map_folder = f'maps/{room.key}' 
            map_paths: list[str] = []
            for name in os.listdir(map_folder):
                map_paths.append(map_folder + '/' + name)
            map_path = random.choice(map_paths)
            new_map = TileMap.load(map_path, self.tileset)
            self.tilemap.place(new_map, room.position, False)
        
        spawn_pos = (0, 0)
        doors = self.tilemap.get_tiles_with_type('door') 
        if doors:
            door: Tile = random.choice(doors)
            spawn_pos = door.pixel_pos
       
        self.p1 = Player(spawn_pos)
        self.players = list[Player]

        self.camera = Camera(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.camera.tilemap = self.tilemap
        self.camera.set_boundary(self.tilemap.get_rect())
        self.camera.add(self.p1)
        self.camera.move_to(self.p1.get_center(), instant=True)

        self.running = False
        self.command_thread = threading.Thread(target=self.handle_commands)
        self.command_thread.daemon = True
    
    def run(self):
        self.running = True
        self.command_thread.start()
        self.handle_game()

    def handle_game(self):
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

            if self.command_active:
                draw_transparent_rect(
                    self.camera.display, 
                    rect=pygame.Rect(0, self.camera.height - 12, self.camera.width, 12),
                    color=(0, 0, 0), 
                    alpha=128
                )
                text = f'{self.command_input}'
                text_surf = self.FONT.render(text, antialias=False, color=(255, 255, 255))
                self.camera.display.blit(text_surf, (4, self.camera.height - 8))


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
                        self.tilemap = TileMap.load(path, self.TYPES)
                    case ['/quit']:
                        self.running = False
                    case ['/collision']:
                        self.p1.collision_enabled = not self.p1.collision_enabled 
                    case ['/jumps', amount]:
                        self.p1.max_jumps = amount
                        self.p1.jumps_remaining = amount
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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SLASH:
                self.command_active = not self.command_active
                self.command_input = ''

            if self.command_active:
                if event.key == pygame.K_RETURN:
                    self.command_active = False
                    self.command_input = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.command_input = self.command_input[:-1]
                else:
                    self.command_input += event.unicode
    
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
    