import os
import random
import pygame
from src.level_gen import CONFIGS, generate_level, Attribute
from src.util import Assets, Vec2, Direction
from src.tilemap import TileMap, Tile
from src.level_gen import LevelMap

MAPS_PATH = 'assets/maps'

class Level:
    current: 'Level' = None

    def __init__(self, seed = None, config = CONFIGS[0], map_path: str = None):
        from .components import Entity, Collider
        from .player import Player 
        from .gravity import Gravity
        
        Level.current = self

        self.entities: list[Entity] = []
        self.colliders: list[Collider] = []

        self.spawn_pos = pygame.Vector2(16, 16)
        self.exit_pos = pygame.Vector2(0, 0)

        if map_path:
            self.tilemap = TileMap.load(map_path, Assets.TILESET)
        else:
            self.tilemap = self.generate(config, seed)
        
        self.spikes = Level._create_spikes(self.tilemap)
        self.entities.extend(self.spikes)
        
        for gravity in self.tilemap.get_tiles_with('gravity'):
            Gravity(gravity.pos)

        self.star_spawner = None
        
        self.player = Player()
        self.entities.append(self.player)
        self.player.spawn(self.spawn_pos)
    
    def register_collider(self, collider: 'Collider'):
        self.colliders.append(collider)

    def unregister_collider(self, collider: 'Collider'):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def get_colliders(self) -> list['Collider']:
        return self.colliders

    def generate(self, config: str, seed: int | str = None, room_size = Vec2(14, 10)) -> None:
        from .exit import Exit

        level_map: LevelMap = generate_level(config, seed)
        tilemap = TileMap(Assets.TILESET, size=Vec2(0, 0))
        self._create_border(tilemap)

        for y in range(level_map.config.rows):
            for x in range(level_map.config.cols):
                room = level_map.get_room_at(Vec2(x, y))

                # if room does not exit at postion (x, y) in level_map, fill 
                if room is None:
                    Level._fill_empty_room(tilemap, Vec2(x, y), room_size)
                    continue
                
                # if room exists at postion (x, y) in level_map
                sub, flip = self._get_folder_flip(room.key)
                map_folder = f'{MAPS_PATH}/{sub}'
                map_paths: list[str] = []
                for name in os.listdir(map_folder):
                    map_paths.append(map_folder + '/' + name)

                map_path = random.choice(map_paths)
                new_map = TileMap.load(map_path, Assets.TILESET)
                
                if room.has_attribute(Attribute.ENTRANCE):
                    pos = random.choice(new_map.get_valid_floor(['stone'])).tile_pos
                    spawn_tile = new_map.create_tile(
                        Assets.TILESET.get_by('entrance'),
                        0,
                        Vec2(pos.x, pos.y - 1)
                    )
                
                if room.has_attribute(Attribute.EXIT):
                    pos = random.choice(new_map.get_valid_floor(['stone'])).tile_pos
                    exit_tile = new_map.create_tile(
                        Assets.TILESET.get_by('exit'), 
                        0, 
                        Vec2(pos.x, pos.y - 1)
                    )
                
                tilemap.place_tilemap(new_map, room.position, flip)
        
        self.spawn_pos = spawn_tile.pos
        self.exit_pos = exit_tile.pos
        Exit(self.exit_pos)

        return tilemap
    
    @staticmethod
    def _create_spikes(tilemap: TileMap) -> list['Spike']:
        """
        Queues for the spike tiles within a TileMap and creates Spike entities for each grouping
        based on three sets, horizontal, vertical, and corner tiles. This greatly reduces the 
        entity/collider count by creating a single entity for a grouping of spikes.
        """
        from .spike import Spike, HSpike, VSpike, CSpike
        spikes: set[Spike] = set()
        horizontal_tiles: set[Tile] = set()
        vertical_tiles: set[Tile] = set()
        corner_tiles: set[Tile] = set()
        
        # categorize all spikes into three sets: horizontal, vertical, and corner
        spike_tiles = tilemap.get_tiles_with('spike')
        for tile in spike_tiles:
            a = []
            for direction in Direction.cardinals():
                adj = tilemap.get_tile(Vec2(tile.tile_pos.x, tile.tile_pos.y), direction)
                a.append(bool(adj and adj.tile_type.name == 'spike'))

            if (a[2] or a[3]) and not (a[0] or a[1]):
                horizontal_tiles.add(tile)
            elif (a[0] or a[1]) and not (a[2] or a[3]):
                vertical_tiles.add(tile)
            else:
                corner_tiles.add(tile)
        
        # create merged spike entities for horizontal set
        visited = set()
        for tile in sorted(horizontal_tiles, key=lambda tile: tile.tile_pos.x):
            if tile in visited:
                continue
            visited.add(tile)

            width = 1
            while tilemap.get_tile(Vec2(tile.tile_pos.x + width, tile.tile_pos.y)) in horizontal_tiles:
                visited.add(tilemap.get_tile(Vec2(tile.tile_pos.x + width, tile.tile_pos.y)))
                width += 1
            
            tile_above = tilemap.get_tile(Vec2(tile.tile_pos.x, tile.tile_pos.y - 1))
            above = tile_above is not None and tile_above.tile_type.name == 'stone'
            spikes.add(HSpike(tile.pos, width, above))
        
        # create merged spike entities for vertical set
        visited.clear()
        for tile in sorted(vertical_tiles, key=lambda tile: tile.tile_pos.y):
            if tile in visited:
                continue
            visited.add(tile)

            height = 1
            while tilemap.get_tile(Vec2(tile.tile_pos.x, tile.tile_pos.y + height)) in vertical_tiles:
                visited.add(tilemap.get_tile(Vec2(tile.tile_pos.x, tile.tile_pos.y + height)))
                height += 1
            
            tile_right = tilemap.get_tile(Vec2(tile.tile_pos.x + 1, tile.tile_pos.y))
            right = tile_right is not None and tile_right.tile_type.name == 'stone'
            spikes.add(VSpike(tile.pos, height, right))

        # create spike entities for corner set
        for tile in corner_tiles:
            tile_above = tilemap.get_tile(Vec2(tile.tile_pos.x, tile.tile_pos.y - 1))
            above = tile_above is not None and tile_above.tile_type.name == 'stone'
            tile_right = tilemap.get_tile(Vec2(tile.tile_pos.x + 1, tile.tile_pos.y))
            right = tile_right is not None and tile_right.tile_type.name == 'stone'
            spikes.add(CSpike(tile.pos, above, right))

        # remove tile object from tilemap now that we have created an entity
        tilemap.remove_tiles(spike_tiles)
        return spikes

    @staticmethod 
    def _create_border(tilemap: TileMap) -> None:
        top = pygame.Rect(0, -1, tilemap.size.x + 2, 1)
        bottom = pygame.Rect(-1, tilemap.size.y, tilemap.size.x + 2, 1)
        left = pygame.Rect(-1, -1, 1, tilemap.size.y + 1)
        right = pygame.Rect(tilemap.size.x, -1, 1, tilemap.size.y + 1)
        tilemap.create_tile_rect(Assets.TILESET.get_by('stone'), top)
        tilemap.create_tile_rect(Assets.TILESET.get_by('stone'), bottom)
        tilemap.create_tile_rect(Assets.TILESET.get_by('stone'), left)
        tilemap.create_tile_rect(Assets.TILESET.get_by('stone'), right)
    
    @staticmethod
    def _fill_empty_room(tilemap: TileMap, room_pos: Vec2, room_size: Vec2) -> None:
        tilemap.create_tile_rect(
            Assets.TILESET.get_by('stone'), 
            pygame.Rect(room_pos.x * room_size.x, room_pos.y * room_size.y, room_size.x, room_size.y)
        )

    @staticmethod
    def _get_folder_flip(key: int) -> tuple[str, bool]:
        match key:
            case 1 | 2:  
                folder = '1_2'
                flip = key == 2
            case 5 | 6:
                folder = '5_6'
                flip = key == 6
            case 9 | 10:
                folder = '9_10'
                flip = key == 10
            case 13 | 14:
                folder = '13_14'
                flip = key == 14
            case _:
                folder = str(key)
                flip = random.choice([True, False])
            
        return folder, flip