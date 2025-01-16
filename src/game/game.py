import sys
import pygame
from src.tilemap import TileMap 
from src.util import Assets, CommandPrompt
from .player import Player, PlayerState
from .camera import Camera
from .map_builder import MapBuilder
from .asteroid import AsteroidSpawner

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

        self.p1 = Player()
        self.camera.add(self.p1)
        self.players = list[Player]

        self.asteroid_spawner = AsteroidSpawner()
   
    def new(self, seed=None):
        self.tilemap =  MapBuilder.generate('configs/1.json', seed)
        self.p1.set_pos(pygame.Vector2(self.tilemap.spawn_tile.pixel_pos))
        self.p1.set_state(PlayerState.AIR)

        self.camera.move_to(self.p1.get_center(), instant=True)
        self.camera.tilemap = self.tilemap
        self.camera.set_boundary(self.tilemap.get_rect())
        
        #self.asteroid_spawner.clear()
        #self.asteroid_spawner.set_boundary(self.tilemap.get_rect())
        #self.asteroid_spawner.spawn(10)
        #self.camera.add(self.asteroid_spawner)
    
    def run(self):
        self.running = True
        self.new()
       
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
                self.command_prompt.handle_event(event)
            
            self.handle_commands()
            
            if not self.command_prompt.enabled:
                self.camera.update()
                self.debug_display()
                
                self.p1.update(self.tilemap)
                self.camera.move_to(self.p1.get_center())
                #self.asteroid_spawner.update()

            # Draw command prompt
            self.command_prompt.render(self.camera.display)

            try:
                self.window.blit(pygame.transform.scale(self.camera.display, self.window.get_size()))
                pygame.display.update()
                self.clock.tick(FPS) 
            except:
                self.running = False

        pygame.quit()
        sys.exit()
    
    def debug_display(self):
        text = f'{self.p1.state_machine.current_state.name}\n'
        text += f'x: {int(self.p1.pos.x):04}, y:{int(self.p1.pos.y):04} \n'
        text += ' '.join(f'{dir_.name[0]}:{int(val)}' for dir_, val in self.p1.collisions.items())
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
                if self.p1.get_state() == PlayerState.GHOST:
                    self.p1.set_state(PlayerState.AIR)
                else:
                    self.p1.set_state(PlayerState.GHOST)
            case ['n']:
                self.new()
            case ['n', seed]:
                self.new(seed)
            case ['p', index]:
                self.p1.load_sprite(int(index))
            case ['tp', x, y]:
                self.p1.pos = pygame.Vector2(int(x), int(y))
            case ['jumps', amount]:
                self.p1.max_jumps = int(amount)
                self.p1.jumps_remaining = self.p1.max_jumps
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
    