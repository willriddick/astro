import sys
import threading
import argparse
import pygame
from src.util import load_image, load_sprite_sheet 
from .tilemap import Tilemap
from .tile_type import TileType
from .tileset import Tileset

RENDER_SCALE = 2
WIDTH, HEIGHT = 400, 300

class Editor:
    
    def __init__(self, args):
        pygame.init()
        pygame.display.set_caption('Editor')
        self.display = pygame.Surface((WIDTH, HEIGHT))
        self.screen = pygame.display.set_mode((WIDTH * RENDER_SCALE, HEIGHT * RENDER_SCALE))
        self.clock = pygame.time.Clock()
        self.running = False
        self.last_path = ''

        self.tileset = Tileset(16)
        self.tileset.add('stone', load_sprite_sheet(load_image('tileset/rock.png'), (16,16)), True)
        self.tileset.add('door', [load_sprite_sheet(load_image('items.png'), (16,16))[0]], False)

        if args.load:
            self.last_path = args.load
            self.tilemap = Tilemap.load(args.load, self.tileset)
        else:
            self.tilemap = Tilemap(self.tileset)

        if args.size:
            self.tilemap.set_size(args.size)
       
        self.camera_direction = (0, 0)
        self.camera_speed = (2, 2)
        self.camera_offset = (0, 0)
    
        self.left_click = False
        self.right_click = False
        self.shift_pressed = False
        self.q_pressed = False
        self.e_pressed = False

        self.command_thread = threading.Thread(target=self.handle_commands)
        self.command_thread.daemon = True

    def run(self):
        print('Running Editor...')
        self.running = True
        self.command_thread.start()
        self.handle_editor()
    
    def handle_commands(self):
        while self.running:
            try:
                command = input()
                match command.split():
                    case ['/help' | '/h']:
                        print('Available commands:')
                        print('/help - Show this help message')
                        print('/save <path> - Save the tilemap to the specified path')
                        print('/load <path> - Load the tilemap from the specified path')
                        print('/clear - Clear the tilemap')
                        print('/quit - Quit the editor\n')
                    case ['/save' | '/s']:
                        if self.last_path:
                            Tilemap.save(self.tilemap, self.last_path)
                    case ['/save' | '/s', path]:
                        Tilemap.save(self.tilemap, path)
                    case ['/load' | '/l', path]:
                        self.last_path = path
                        self.tilemap = Tilemap.load(path, self.TYPES)
                    case ['/clear' | '/c']: 
                        self.tilemap.clear()
                        print(f'Tilemap cleared')
                    case ['/size' | '/z', width, height]:
                        self.tilemap.set_size((int(width), int(height)))
                    case ['/place', path, x, y, flip]:
                        room = Tilemap.load(path, self.TYPES)
                        self.tilemap.place(room, (int(x), int(y)), flip.lower().startswith('t'))
                    case ['/quit' | '/q']:
                        self.running = False
                    case _:
                        print(f'Unknown command: {command}')
                        print('Type /help for a list of commands')
            except EOFError:
                self.running = False
            except KeyboardInterrupt:
                self.running = False
    
    def handle_editor(self):
        mouse_pos = (0, 0)
        tile_pos = (0, 0)
        type_index = 0
        tile_type: TileType = self.tileset.get_by_index(type_index)
        tile_variant = 0

        while self.running:
            self.display.fill((0, 0, 0, 0))
            for event in pygame.event.get():
                self.handle_event(event)
            
            # Calculate mouse position
            mouse_pos = (
                pygame.mouse.get_pos()[0] / RENDER_SCALE, 
                pygame.mouse.get_pos()[1] / RENDER_SCALE
            )

            # Calculate selected tile position
            tile_pos = (
                int((mouse_pos[0] + self.camera_offset[0]) // self.tileset.tile_size), 
                int((mouse_pos[1] + self.camera_offset[1]) // self.tileset.tile_size)
            )

            # Change tile type and variant
            if self.q_pressed or self.e_pressed:
                direction = -1 if self.q_pressed else 1
                self.q_pressed = False
                self.e_pressed = False

                if self.shift_pressed:
                    tile_variant = (tile_variant + direction) % len(tile_type.images)
                else:
                    type_index = self.tileset.get_by_index(type_index + direction)
                    tile_type = self.TYPES[type_index]
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
        
        print('Exiting...')
        pygame.quit()
        sys.exit()
    
    def move_camera(self):
        keys = pygame.key.get_pressed()
        self.camera_direction = (
            keys[pygame.K_d] - keys[pygame.K_a],
            keys[pygame.K_s] - keys[pygame.K_w]
        )
        self.camera_offset = (
            round(self.camera_offset[0] + self.camera_direction[0] * self.camera_speed[0]),
            round(self.camera_offset[1] + self.camera_direction[1] * self.camera_speed[1])
        )
    
    def draw_tile_square(self, tile_pos):
        tile_size = self.tileset.tile_size
        current_tile = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
        current_tile.set_alpha(100)
        pygame.draw.rect(
            current_tile, (255, 255, 255),
            (0, 0, tile_size, tile_size), 1
        )
        self.display.blit(
            current_tile, 
            (tile_pos[0] * tile_size - self.camera_offset[0], 
            tile_pos[1] * tile_size - self.camera_offset[1])
        )
    
    def draw_border(self):
        tile_size = self.tileset.tile_size
        size = self.tilemap.size
        border = pygame.Surface((size[0] * tile_size, size[1] * tile_size), pygame.SRCALPHA)
        border.set_alpha(100)
        pygame.draw.rect(
            border, (255, 0, 0),
            (0, 0, size[0] * tile_size, size[1] * tile_size), 1
        )
        self.display.blit(border, (-self.camera_offset[0], -self.camera_offset[1]))
    
    def handle_event(self, event: pygame.Event):
        if event.type == pygame.QUIT:
            self.running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                self.shift_pressed = True
            if event.key == pygame.K_q:
                self.q_pressed = True
            if event.key == pygame.K_e:
                self.e_pressed = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                self.shift_pressed = False
            if event.key == pygame.K_q:
                self.q_pressed = False
            if event.key == pygame.K_e:
                self.e_pressed = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.left_click = True
            if event.button == 3:
                self.right_click = True
        if event.type == pygame.MOUSEBUTTONUP: 
            if event.button == 1:
                self.left_click = False
            if event.button == 3:
                self.right_click = False

def parse_tuple(s):
    try:
        return tuple(map(int, s.split(',')))
    except ValueError:
        raise argparse.ArgumentTypeError("Tuple must be in the form \"int,int\"")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Editor')
    parser.add_argument('-l', '--load', type=str, help='Load a tilemap from a file')
    parser.add_argument('-s', '--size', type=parse_tuple, help='Set the level size')
    args = parser.parse_args()

    editor = Editor(args)
    editor.run()
