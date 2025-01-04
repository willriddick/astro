import struct
import pygame
from src.util import Direction
from .tile import Tile
from .tile_type import TileType

HEADER_FORMAT = 'hhh' # tile_size, border_width, border_height
TILE_FORMAT = '16s hhh' # type, variant, x, y

class Tilemap:
    def __init__(self, types: list[TileType], tile_size: int = 16, size: tuple[int, int]=(0, 0), debug: bool = False):
        self.types = types
        self.tile_size = tile_size
        self.size = size
        self.map: dict[tuple[int, int], Tile] = {}
        self.debug = debug
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, self.size[0] * self.tile_size, self.size[1] * self.tile_size)

    def set_size(self, size: tuple[int, int]):
        self.size = size
    
    def clear(self):
        self.map = {}
    
    def render(self, surf: pygame.Surface, offset=(0, 0)):
        for tile in self.map.values():
            tile.render(surf, offset)
    
    def get_tile_type(self, name: str) -> TileType:
        for type in self.types:
            if type.name == name:
                return type
        return None
    
    def get_tile(self, tile_pos: tuple[int, int], direction: Direction = Direction.NONE) -> Tile | None:
        new_pos = (tile_pos[0] + direction.value[0], tile_pos[1] + direction.value[1])
        return self.map.get(new_pos)
    
    def get_tiles_with_type(self, type: str) -> list[Tile]:
        output = []
        for tile in self.map.values():
            if tile.type.name == type:
                output.append(tile)
        return output
    
    def get_tiles_around(self, tile_pos: tuple[int, int], filter: list[str]) -> list[Tile]:
        tiles = []
        for direction in Direction:
            tile = self.get_tile(tile_pos, direction)
            if tile and tile.type.name in filter:
                tiles.append(tile)
        return tiles
    
    def create_tile(self, type: TileType, variant: int, tile_pos: tuple[int, int]):
        x, y = tile_pos
        if not (0 <= x < self.size[0] and 0 <= y < self.size[1]):
            return

        if tile_pos in self.map:
            self.remove_tile(tile_pos)
        new_tile = Tile(self, type, variant, tile_pos)
        self.map[tile_pos] = new_tile
        self._update_autotiles_around(tile_pos)
                
    def remove_tile(self, tile_pos: tuple[int, int]):
        if tile := self.get_tile(tile_pos):
            del self.map[tile.tile_pos]
            self._update_autotiles_around(tile_pos)
    
    def flip(self):
        new_map = {}
        for (x, y), tile in self.map.items():
            new_x = self.size[0] - x - 1
            new_map[(new_x, y)] = tile
            tile.tile_pos = (new_x, y)
        self.map = new_map
    
    def place(self, room: 'Tilemap', offset: tuple[int, int], flip: bool):
        x_start = offset[0] * room.size[0]
        y_start = offset[1] * room.size[1]
        self.size = (
            max(self.size[0], room.size[0] * (offset[0] + 1)), 
            max(self.size[1], room.size[1] * (offset[1] + 1))
        )

        if flip:
            room.flip()

        for tile in room.map.values():
            new_pos = (x_start + tile.tile_pos[0], y_start + tile.tile_pos[1])
            self.create_tile(tile.type, tile.variant, new_pos)

    def _update_autotiles_around(self, tile_pos: tuple[int, int]):
        for direction in Direction:
            tile = self.get_tile(tile_pos, direction)
            if tile and tile.type.autotile:
                self._autotile(tile)

    def _autotile(self, tile: Tile):
        pos = tile.tile_pos
        name = tile.type.name

        # Edge detection (No bit shifting yet)
        u = int(self.get_tile(pos, Direction.UP) is not None and self.get_tile(pos, Direction.UP).type.name == name)
        r = int(self.get_tile(pos, Direction.RIGHT) is not None and self.get_tile(pos, Direction.RIGHT).type.name == name)
        d = int(self.get_tile(pos, Direction.DOWN) is not None and self.get_tile(pos, Direction.DOWN).type.name == name)
        l = int(self.get_tile(pos, Direction.LEFT) is not None and self.get_tile(pos, Direction.LEFT).type.name == name)

        # Calculate edges bitmask (bit shifting happens here)
        edges = u | (r << 1) | (d << 2) | (l << 3)

        # Corner detection (must match GameMaker logic)
        ul = int(u and l and self.get_tile(pos, Direction.UP_LEFT) is not None and self.get_tile(pos, Direction.UP_LEFT).type.name == name)
        ur = int(u and r and self.get_tile(pos, Direction.UP_RIGHT) is not None and self.get_tile(pos, Direction.UP_RIGHT).type.name == name)
        dr = int(d and r and self.get_tile(pos, Direction.DOWN_RIGHT) is not None and self.get_tile(pos, Direction.DOWN_RIGHT).type.name == name)
        dl = int(d and l and self.get_tile(pos, Direction.DOWN_LEFT) is not None and self.get_tile(pos, Direction.DOWN_LEFT).type.name == name)

        # Calculate corners bitmask
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
    def save(tilemap, path: str):
        try:
            with open(path, 'wb') as f:
                f.write(struct.pack(HEADER_FORMAT, tilemap.tile_size, *tilemap.size))
                for tile in tilemap.map.values():
                    f.write(struct.pack(
                        TILE_FORMAT, tile.type.name.encode(), tile.variant, *tile.tile_pos
                    ))
            print(f'Tilemap saved to {path}')
        except FileNotFoundError:
            print(f'Save failed... file not found: {path}')
    
    @staticmethod
    def load(path: str, types: list[TileType]) -> 'Tilemap':
        try:
            with open(path, 'rb') as f:
                content = f.read()

            header_offset = struct.calcsize(HEADER_FORMAT)
            tile_size, *size = struct.unpack(HEADER_FORMAT, content[:header_offset])
            tilemap = Tilemap(types, tile_size, tuple(size))

            step = struct.calcsize(TILE_FORMAT)
            for offset in range(header_offset, len(content), step):
                data = struct.unpack(TILE_FORMAT, content[offset:offset + step])
                type = tilemap.get_tile_type(data[0].decode().rstrip('\00'))
                tilemap.create_tile(type, data[1], (data[2], data[3]))

            return tilemap
        except FileNotFoundError:
            print(f'File not found: {path}')
