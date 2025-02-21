import os
import sys
import pygame
from src.util import Vec2, CommandPrompt
import src.assets as assets
from .tile_map import TileMap
from .tile_type import TileType

RENDER_SCALE = 3
DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180

MAP_PATH = os.path.join('assets', 'maps')

class Editor:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Editor')
        
        self.running = False
        self.clock = pygame.time.CLOCK()
        self.last_path = ''
        self.command_prompt = CommandPrompt()

        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH * RENDER_SCALE, DISPLAY_HEIGHT * RENDER_SCALE))
        assets.load()

        self.tilemap = TileMap(assets.TILESET)

        self.camera_direction = Vec2(0, 0)
        self.camera_speed = Vec2(2, 2)
        self.camera_offset = pygame.Vector2(0, 0)
    
        self.left_click = False
        self.right_click = False
        self.shift_pressed = False
        self.q_pressed = False
        self.e_pressed = False

        self.mouse_pos = Vec2(0, 0)
        self.tile_pos = Vec2(0, 0)
        self.type_index = 0
        self.tile_type: TileType = assets.TILESET.get_by_index(self.type_index)
        self.tile_variant = 0

    def run(self):
        self.running = True

        while self.running:
            self.display.fill((0, 0, 0, 0))

            for event in pygame.event.get():
                self.handle_event(event)
                self.command_prompt.handle_event(event)
            
            self.handle_commands()

            if not self.command_prompt.enabled:
                self.handle_editing()

            # Render tilemap
            self.tilemap.render(self.display, self.camera_offset)

            # Render selected tile
            selected_tile = self.tile_type.images[self.tile_variant].copy()
            selected_tile.set_alpha(100)
            self.display.blit(selected_tile, (0, 0))

            # Draw current tile position
            self.draw_tile_square(self.tile_pos)

            # Draw border
            self.draw_border()

            # Draw command prompt
            self.command_prompt.render(self.display)

            try:
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()))
                pygame.display.update()
                self.clock.tick(60) 
            except:
                self.running = False
        
        pygame.quit()
        sys.exit()
    
    def handle_editing(self):
        # Calculate mouse position
        self.mouse_pos = Vec2(
            pygame.mouse.get_pos()[0] // RENDER_SCALE,
            pygame.mouse.get_pos()[1] // RENDER_SCALE
        )

        # Calculate selected tile position
        self.tile_pos = Vec2(
            int((self.mouse_pos.x + self.camera_offset[0]) // assets.TILESET.tile_size.x), 
            int((self.mouse_pos.y + self.camera_offset[1]) // assets.TILESET.tile_size.y)
        )

        # Change tile type and variant
        if self.q_pressed or self.e_pressed:
            direction = -1 if self.q_pressed else 1
            self.q_pressed = False
            self.e_pressed = False

            if self.shift_pressed:
                self.tile_variant = (self.tile_variant + direction) % len(self.tile_type.images)
            else:
                self.type_index += direction
                self.tile_type = assets.TILESET.get_by_index(self.type_index)
                self.tile_variant = 0

        # Create or remove tile
        if self.left_click:
            self.tilemap.create_tile(self.tile_type, self.tile_variant, self.tile_pos)
        
        if self.right_click:
            self.tilemap.remove_tile(self.tile_pos)
        
        # Update display
        self.move_camera() 

    def handle_commands(self):
        command = self.command_prompt.pop_command()
        if command == '': 
            return

        match command.split():
            case ['help' | 'h']:
                print('Available commands:')
                print('/help - Show this help message')
                print('/save <path> - Save the tilemap to the specified path')
                print('/load <path> - Load the tilemap from the specified path')
                print('/clear - Clear the tilemap')
                print('/quit - Quit the editor\n')
            case ['save' | 's']:
                if self.last_path:
                    TileMap.save(self.tilemap, self.last_path)
            case ['save' | 's', path]:
                TileMap.save(self.tilemap, os.path.join(MAP_PATH, path))
            case ['load' | 'l', path]:
                self.last_path = os.path.join(MAP_PATH, path)
                tilemap = TileMap.load(self.last_path, assets.TILESET)
                if tilemap:
                    self.tilemap = tilemap
            case ['clear' | 'c']: 
                self.tilemap.clear()
                print(f'Tilemap cleared')
            case ['size' | 'z', width, height]:
                self.tilemap.set_size(Vec2(int(width), int(height)))
            case ['quit' | 'q']:
                self.running = False
            case _:
                print(f'Unknown command: {command}')

    def move_camera(self):
        keys = pygame.key.get_pressed()
        self.camera_direction = Vec2(
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )
        self.camera_offset = pygame.Vector2(
            round(self.camera_offset.x + self.camera_direction.x * self.camera_speed.x),
            round(self.camera_offset.y + self.camera_direction.y * self.camera_speed.y)
        )
    
    def draw_tile_square(self, tile_pos):
        tile_size = assets.TILESET.tile_size
        current_tile = pygame.Surface((tile_size.x, tile_size.y), pygame.SRCALPHA)
        current_tile.set_alpha(100)
        pygame.draw.rect(
            current_tile, (255, 255, 255),
            (0, 0, tile_size.x, tile_size.y), 1
        )
        self.display.blit(
            current_tile, 
            (tile_pos.x * tile_size.x - self.camera_offset.x, 
            tile_pos.y * tile_size.y - self.camera_offset.y)
        )
    
    def draw_border(self):
        tile_size = assets.TILESET.tile_size
        size = self.tilemap.size
        border = pygame.Surface((size.x * tile_size.x, size.y * tile_size.y), pygame.SRCALPHA)
        border.set_alpha(100)
        pygame.draw.rect(
            border, (255, 0, 0),
            (0, 0, size.x * tile_size.x, size.y * tile_size.y), 1
        )
        self.display.blit(border, (-self.camera_offset.x, -self.camera_offset.y))
    
    def handle_event(self, event: pygame.Event):
        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                self.shift_pressed = True
            elif event.key == pygame.K_q:
                self.q_pressed = True
            elif event.key == pygame.K_e:
                self.e_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.shift_pressed = False
            elif event.key == pygame.K_q:
                self.q_pressed = False
            elif event.key == pygame.K_e:
                self.e_pressed = False

        # Handle mouse button events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_click = True
            elif event.button == 3:
                self.right_click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.left_click = False
            elif event.button == 3:
                self.right_click = False
