import struct
import pygame
from src.util import Direction
from .tile_set import TileSet
from .tile import Tile
from .tile_type import TileType
from src.util import Vec2

HEADER_FORMAT = 'hhh' # tile_size, border_width, border_height
TILE_FORMAT = '16s hhh' # type, variant, x, y

class TileMap:
    def __init__(self, tileset: TileSet, size: Vec2=Vec2(0,0), debug: bool = False):
        self.tileset = tileset
        self.size = size
        self.map: dict[Vec2, Tile] = {}
        self.debug = debug

        self.spawn_tile = None
    
    @property
    def tile_size(self) -> int:
        return self.tileset.tile_size
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, self.size.x * self.tile_size, self.size.y * self.tile_size)

    def set_size(self, size: Vec2):
        self.size = size
    
    def clear(self):
        self.map = {}
    
    def render(self, surf: pygame.Surface, offset: pygame.Vector2):
        for tile in self.map.values():
            tile.render(surf, offset)
    
    def get_tile(self, tile_pos: Vec2, offset: Direction = Direction.NONE) -> Tile | None:
        new_pos = Vec2(tile_pos.x + offset.value.x, tile_pos.y + offset.value.y)
        return self.map.get(new_pos)
    
    def get_tiles_with_type(self, type: str) -> list[Tile]:
        return list(filter(lambda x: x.type.name == type, self.map.values))
    
    def get_tiles_around(self, tile_pos: Vec2, filter_: list[str]) -> list[Tile]:
        tiles = []
        for direction in Direction:
            tile = self.get_tile(tile_pos, direction)
            if tile and tile.type.name in filter_:
                tiles.append(tile)
        return tiles
    
    def create_tile(self, type: TileType, variant: int, tile_pos: Vec2) -> Tile:
        if tile_pos in self.map:
            self.remove_tile(tile_pos)
        new_tile = Tile(self, type, variant, tile_pos)
        self.map[tile_pos] = new_tile
        self._update_autotiles_around(tile_pos)

        return new_tile
    
    def remove_tile(self, tile_pos: Vec2):
        if tile := self.get_tile(tile_pos):
            del self.map[tile.tile_pos]
            self._update_autotiles_around(tile_pos)
    
    def flip_x(self):
        new_map = {}
        for pos, tile in self.map.items():
            new_x = self.size.x - pos.x - 1
            new_map[(new_x, pos.y)] = tile
            tile.tile_pos = (new_x, pos.y)
        self.map = new_map
    
    def get_valid_floor(self, filter_: list[str]) -> list[Tile]:
        output = []
        for tile in self.map.values():
            if tile.type.name in filter_:
                x, y = tile.tile_pos
                if (
                    self.get_tile((x, y - 1)) is None 
                    and y - 1 >= 0
                    and x > 0 
                    and x < self.size[0] - 1
                ):
                    output.append(tile)
        return output
    
    def place_tile(self, tile: Tile, new_pos: Vec2):
        tile.tile_pos = new_pos
        self.map[new_pos] = tile
        if tile.type.autotile:
            self._update_autotiles_around(new_pos)
    
    def place_tilemap(self, tilemap: 'Tilemap', offset: Vec2, flip: bool):
        x_start = offset.x * tilemap.size.x
        y_start = offset.y * tilemap.size.y
        self.size = (
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
    def load(path: str, tileset: TileSet) -> 'TileMap':
        try:
            with open(path, 'rb') as f:
                content = f.read()

            header_offset = struct.calcsize(HEADER_FORMAT)
            tile_size, *size = struct.unpack(HEADER_FORMAT, content[:header_offset])
            tilemap = TileMap(tileset, size)

            step = struct.calcsize(TILE_FORMAT)
            for offset in range(header_offset, len(content), step):
                data = struct.unpack(TILE_FORMAT, content[offset:offset + step])
                type = tileset.get_by_name(data[0].decode().rstrip('\00'))
                tilemap.create_tile(type, data[1], Vec2(data[2], data[3]))

            return tilemap
        except FileNotFoundError:
            print(f'File not found: {path}')
