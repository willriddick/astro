import sys
import argparse
import pygame
from src.util import Assets, Vec2
from .tile_map import TileMap
from .tile_type import TileType

RENDER_SCALE = 3
DISPLAY_WIDTH, DISPLAY_HEIGHT = 320, 180

class Editor:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Editor')
        
        self.running = False
        self.clock = pygame.time.Clock()
        self.last_path = ''

        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.screen = pygame.display.set_mode((DISPLAY_WIDTH * RENDER_SCALE, DISPLAY_HEIGHT * RENDER_SCALE))
        Assets.load_assets()

        self.tilemap = TileMap(Assets.TILESET)

        self.camera_direction = Vec2(0, 0)
        self.camera_speed = Vec2(2, 2)
        self.camera_offset = pygame.Vector2(0, 0)
    
        self.left_click = False
        self.right_click = False
        self.shift_pressed = False
        self.q_pressed = False
        self.e_pressed = False
    
    def run(self):
        mouse_pos = Vec2(0, 0)
        tile_pos = Vec2(0, 0)
        type_index = 0
        tile_type: TileType = Assets.TILESET.get_by_index(type_index)
        tile_variant = 0
        self.running = True

        while self.running:
            self.display.fill((0, 0, 0, 0))

            for event in pygame.event.get():
                self.handle_event(event)

            # Calculate mouse position
            mouse_pos = Vec2(
                pygame.mouse.get_pos()[0] / RENDER_SCALE, 
                pygame.mouse.get_pos()[1] / RENDER_SCALE
            )

            # Calculate selected tile position
            tile_pos = Vec2(
                int((mouse_pos.x + self.camera_offset[0]) // Assets.TILESET.tile_size.x), 
                int((mouse_pos.y + self.camera_offset[1]) // Assets.TILESET.tile_size.y)
            )

            # Change tile type and variant
            if self.q_pressed or self.e_pressed:
                direction = -1 if self.q_pressed else 1
                self.q_pressed = False
                self.e_pressed = False

                if self.shift_pressed:
                    tile_variant = (tile_variant + direction) % len(tile_type.images)
                else:
                    type_index = type_index + direction
                    tile_type = Assets.TILESET.get_by_index(type_index)
                    tile_variant = 0

            # Create or remove tile
            if self.left_click:
                self.tilemap.create_tile(tile_type, tile_variant, tile_pos)
            
            if self.right_click:
                self.tilemap.remove_tile(tile_pos)

            # Render tilemap
            self.tilemap.render(self.display, self.camera_offset)

            # Render selected tile
            selected_tile = tile_type.images[tile_variant].copy()
            selected_tile.set_alpha(100)
            self.display.blit(selected_tile, (0, 0))

            # Draw current tile position
            self.draw_tile_square(tile_pos)

            # Draw border
            self.draw_border()

            # Update display
            self.move_camera() 

            try:
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()))
                pygame.display.update()
                self.clock.tick(60) 
            except:
                self.running = False
        
        pygame.quit()
        sys.exit()
    
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
        tile_size = Assets.TILESET.tile_size
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
        tile_size = Assets.TILESET.tile_size
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

def parse_tuple(s):
    try:
        return Vec2(map(int, s.split(',')))
    except ValueError:
        raise argparse.ArgumentTypeError("Tuple must be in the form \"int,int\"")

Editor().run()
