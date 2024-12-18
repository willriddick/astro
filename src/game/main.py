import os
import sys
import threading

import pygame

from ..tilemap.tilemap import Tilemap
from ..tilemap.tilemap import Asset

from .player import Player
from .util import load_images, load_image

FPS = 60

WINDOW_SCALE = 3
DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180
ASPECT_RATIO = DISPLAY_WIDTH / DISPLAY_HEIGHT

class Main:
    def __init__(self):
        pygame.init()

        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * WINDOW_SCALE, DISPLAY_HEIGHT * WINDOW_SCALE),
            pygame.RESIZABLE)
        self.fullscreen = False
        
        self.ASSETS = {
            'stone': Asset('stone', load_images('test-tileset'), True),
        }

        pygame.display.set_caption('GAME')
        pygame.display.set_icon(load_image('player.png'))

        self.clock = pygame.time.Clock()
        
        self.camera_offset = (0, 0)

        self.p1 = Player((self.display.get_width() // 2, self.display.get_height() // 2))
        self.players = pygame.sprite.Group()
        self.players.add(self.p1)

        self.running = True

        self.command_thread = threading.Thread(target=self.handle_commands)
        self.command_thread.daemon = True
        self.command_thread.start()

        self.tilemap: Tilemap = None

        self.handle_game()

    def handle_game(self):
        self.tilemap = Tilemap.load('test', self.ASSETS)

        while self.running:
            self.display.fill((0, 0, 0, 0))
            for event in pygame.event.get():
                self.handle_event(event)
            
            self.tilemap.render(self.display, self.camera_offset)
            for player in self.players:
                player.update(self.tilemap)
                player.render(self.display, self.camera_offset)

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
                        print('/quit - Quit the game')
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
    
if __name__ == "__main__":
    main = Main()
