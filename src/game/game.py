import sys
import pygame
from src.tilemap import TileMap 
from src.util import Assets, CommandPrompt
from .level import Level
from .player import Player, PlayerState
from .camera import Camera

FPS = 60
WINDOW_SCALE = 4
DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180
ASPECT_RATIO = DISPLAY_WIDTH / DISPLAY_HEIGHT

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('GAME')

        self.running = False
        self.clock = pygame.time.Clock()
        self.command_prompt = CommandPrompt()

        self.window = pygame.display.set_mode(
            (DISPLAY_WIDTH * WINDOW_SCALE, DISPLAY_HEIGHT * WINDOW_SCALE),
            pygame.RESIZABLE
        )
        self.camera = Camera(DISPLAY_WIDTH, DISPLAY_HEIGHT)
        self.fullscreen = False
        Assets.load_assets()

        self.level = Level(map_path='maps/10x8/1_2/test')
        self.camera.level = self.level
        self.camera.set_boundary(self.level.tilemap.rect)

        self.player = Player(self.level)
        self.player.spawn(self.level.spawn_pos)
        self.camera.move_to(self.level.spawn_pos, instant=True)

        self.level.entities.append(self.player)
    
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
                self.clock.tick(FPS) 
            except:
                self.running = False

        pygame.quit()
        sys.exit()
    
    def debug_display(self):
        text = f'{self.player.state_machine.current_state.name}\n'
        text += f'x: {int(self.player.pos.x):04}, y:{int(self.player.pos.y):04} \n'
        text += ' '.join(f'{dir_.name[0]}:{int(val)}' for dir_, val in self.player.collisions.items())
        text_surf = Assets.FONT.render(text, antialias=False, color=(255, 255, 255))
        self.camera.display.blit(text_surf, (0, 0))

    def handle_commands(self):
        command = self.command_prompt.pop_command()
        if command == '': 
            return

        match command.split():
            case ['load', path]:
                self.tilemap = TileMap.load(path, self.TYPES)
            case ['g']:
                if self.player.get_state() == PlayerState.GHOST:
                    self.player.set_state(PlayerState.AIR)
                else:
                    self.player.set_state(PlayerState.GHOST)
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
    