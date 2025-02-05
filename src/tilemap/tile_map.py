import json
import pygame
from src.util import Direction, Vec2
from .tile_set import TileSet
from .tile import Tile
from .tile_type import TileType

HEADER_FORMAT = 'hhh' # tile_size, border_width, border_height
TILE_FORMAT = '16s hhh' # type, variant, x, y

class TileMap:
    def __init__(self, tileset: TileSet, size: Vec2=Vec2(0,0)):
        self.tileset = tileset
        self.size = size
        self.map: dict[Vec2, Tile] = {}

    @property
    def tile_size(self) -> Vec2:
        return self.tileset.tile_size
    
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, self.size.x * self.tile_size.x, self.size.y * self.tile_size.y)

    def set_size(self, size: Vec2) -> None:
        self.size = size
    
    def clear(self) -> None:
        self.map = {}
    
    def render(self, surf: pygame.Surface, offset: pygame.Vector2) -> None:
        for tile in self.map.values():
            tile.render(surf, offset)
    
    def get_tile(self, tile_pos: Vec2, offset: Direction = Direction.NONE) -> Tile | None:
        return self.map.get(Vec2.translate(tile_pos, offset))
    
    def get_tiles_with(self, tile_type: str) -> list[Tile]:
        return list(filter(lambda x: x.tile_type.name == tile_type, list(self.map.values())))
    
    def get_tiles_around(self, tile_pos: Vec2) -> list[Tile]:
        return [tile for direction in Direction if (tile := self.get_tile(tile_pos, direction)) is not None]
    
    def create_tile(self, tile_type: TileType, variant: int, tile_pos: Vec2) -> Tile:
        if tile_pos in self.map:
            self.remove_tile(tile_pos)
        new_tile = Tile(self, tile_type, variant, tile_pos)
        self.map[tile_pos] = new_tile
        self._update_autotiles_around(tile_pos)

        return new_tile
    
    def create_tile_rect(self, tile: Tile, rect: pygame.Rect) -> None:
        for y in range(rect.y, rect.y + rect.height):
            for x in range(rect.x, rect.x + rect.width):
                self.create_tile(tile, 0, Vec2(x, y))
    
    def remove_tile(self, tile_pos: Vec2) -> None:
        if tile := self.get_tile(tile_pos):
            del self.map[tile.tile_pos]
            self._update_autotiles_around(tile_pos)
    
    def flip_x(self) -> None:
        new_map = {}
        for pos, tile in self.map.items():
            new_x = self.size.x - pos.x - 1
            new_map[Vec2(new_x, pos.y)] = tile
            tile.tile_pos = Vec2(new_x, pos.y)
        self.map = new_map
    
    def get_valid_floor(self, filter_: list[str]) -> list[Tile]:
        output = []
        for tile in self.map.values():
            if tile.tile_type.name in filter_:
                x, y = tile.tile_pos
                if (
                    self.get_tile(Vec2(x, y - 1)) is None
                    and y - 1 >= 0
                    and 0 < x < self.size.x - 1
                ):
                    output.append(tile)
        return output
    
    def place_tile(self, tile: Tile, new_pos: Vec2) -> None:
        tile.tile_pos = new_pos
        self.map[new_pos] = tile
        if tile.tile_type.autotile:
            self._update_autotiles_around(new_pos)
    
    def place_tilemap(self, tilemap: 'Tilemap', offset: Vec2, flip: bool) -> None:
        x_start = offset.x * tilemap.size.x
        y_start = offset.y * tilemap.size.y
        self.size = Vec2(
            max(self.size.x, tilemap.size.x * (offset.x + 1)), 
            max(self.size.y, tilemap.size.y * (offset.y + 1))
        )

        if flip:
            tilemap.flip_x()

        for tile in tilemap.map.values():
            new_pos = Vec2(x_start + tile.tile_pos.x, y_start + tile.tile_pos.y)
            self.place_tile(tile, new_pos)

    def _update_autotiles_around(self, tile_pos: Vec2):
        for direction in Direction:
            tile = self.get_tile(tile_pos, direction)
            if tile and tile.tile_type.autotile:
                self._autotile(tile)

    def _autotile(self, tile: Tile):
        pos = tile.tile_pos
        name = tile.tile_type.name

        # Get surrounding tiles
        tile_up = self.get_tile(pos, Direction.UP)
        tile_right = self.get_tile(pos, Direction.RIGHT)
        tile_down = self.get_tile(pos, Direction.DOWN)
        tile_left = self.get_tile(pos, Direction.LEFT)
        tile_up_left = self.get_tile(pos, Direction.UP_LEFT)
        tile_up_right = self.get_tile(pos, Direction.UP_RIGHT)
        tile_down_right = self.get_tile(pos, Direction.DOWN_RIGHT)
        tile_down_left = self.get_tile(pos, Direction.DOWN_LEFT)

        # Edge detection
        u = int(tile_up is not None and tile_up.tile_type.name == name)
        r = int(tile_right is not None and tile_right.tile_type.name == name)
        d = int(tile_down is not None and tile_down.tile_type.name == name)
        l = int(tile_left is not None and tile_left.tile_type.name == name)

        # Corner detection
        ul = int(u and l and tile_up_left is not None and tile_up_left.tile_type.name == name)
        ur = int(u and r and tile_up_right is not None and tile_up_right.tile_type.name == name)
        dr = int(d and r and tile_down_right is not None and tile_down_right.tile_type.name == name)
        dl = int(d and l and tile_down_left is not None and tile_down_left.tile_type.name == name)

        # Calculate bitmasks
        edges = u | (r << 1) | (d << 2) | (l << 3)
        corners = ul | (ur << 1) | (dr << 2) | (dl << 3)

        # Determine the correct variant
        variant = {
            0: 0, 1: 1, 2: 2, 3: {0: 3, 2: 4}.get(corners, 3),
            4: 5, 5: 6, 6: {0: 7, 4: 8}.get(corners, 7),
            7: {0: 9, 2: 10, 4: 11, 6: 12}.get(corners, 9),
            8: 13, 9: {0: 14, 1: 15}.get(corners, 14),
            10: 16, 11: {0: 17, 1: 18, 2: 19, 3: 20}.get(corners, 17),
            12: {0: 21, 8: 22}.get(corners, 21),
            13: {0: 23, 1: 24, 8: 25, 9: 26}.get(corners, 23),
            14: {0: 27, 4: 28, 8: 29, 12: 30}.get(corners, 27),
            15: {
                0: 31, 1: 32, 2: 33, 3: 34, 4: 35, 5: 36, 6: 37, 7: 38,
                8: 39, 9: 40, 10: 41, 11: 42, 12: 43, 13: 44, 14: 45, 15: 46
            }.get(corners, 31)
        }.get(edges, 0)

        # Update variant
        tile.variant = variant
  
    @staticmethod
    def save(tilemap: 'Tilemap', path: str):
        try:
            tilemap_data = {
                'size': list(tilemap.size),
                'tiles': []
            }

            for tile in tilemap.map.values():
                tile_data = {
                    't': tile.tile_type.name,
                    'v': tile.variant,
                    'p': [tile.tile_pos.x,  tile.tile_pos.y]
                }
                tilemap_data['tiles'].append(tile_data)

            # Write data to JSON file
            with open(path, 'w') as f:
                json.dump(tilemap_data, f, separators=(',', ':'))

            print(f'Tilemap saved to {path}')
        except FileNotFoundError:
            print(f'Save failed... path not found: {path}')
        except PermissionError:
            print(f'Save failed... permission error on: {path}')
    
    @staticmethod
    def load(path: str, tileset: TileSet) -> 'TileMap':
        try:
            # Read data from JSON file
            with open(path, 'r') as f:
                tilemap_data = json.load(f)

            print(f'Tilemap loaded from {path}')

            # Reconstruct tilemap from data
            tilemap = TileMap(tileset, Vec2(*tilemap_data['size']))

            for tile_data in tilemap_data['tiles']:
                tile_type = tileset.get_by(tile_data['t'])
                pos_data = tile_data['p']
                if isinstance(pos_data, list):
                    tile_pos = Vec2(pos_data[0], pos_data[1])
                else:
                    tile_pos = Vec2(pos_data['x'], pos_data['y'])
                tilemap.create_tile(tile_type, tile_data['v'], tile_pos)

            return tilemap
        except FileNotFoundError:
            print(f'Load failed... path not found: {path}')
        except PermissionError:
            print(f'Load failed... permission error on: {path}')
