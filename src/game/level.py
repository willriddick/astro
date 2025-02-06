import os
import random
import pygame
from src.level_gen import CONFIGS, generate_level, Attribute
from src.util import Assets, Vec2
from src.tilemap import TileMap
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
        from .spike import Spike, HSpike, VSpike, CSpike
        spikes: list[Spike] = []

        spike_tiles = {tile.tile_pos: tile for tile in tilemap.get_tiles_with('spike')}
        visited = set()

        for tile_pos, tile in spike_tiles.items():
            if tile_pos in visited:
                continue  # Skip already processed tiles

            x, y = tile_pos.x, tile_pos.y
            width, height = 1, 1
            visited.add(tile_pos)

            # Neighbor checks
            left = Vec2(x - 1, y) in spike_tiles
            right = Vec2(x + 1, y) in spike_tiles
            above = Vec2(x, y - 1) in spike_tiles
            below = Vec2(x, y + 1) in spike_tiles

            solid_above = tilemap.get_tile(Vec2(x, y - 1))
            solid_below = tilemap.get_tile(Vec2(x, y + 1))
            solid_left = tilemap.get_tile(Vec2(x - 1, y))
            solid_right = tilemap.get_tile(Vec2(x + 1, y))

            is_ceiling = solid_above is not None and solid_above.tile_type.name == 'stone' if solid_above else False
            is_floor = solid_below is not None and solid_below.tile_type.name == 'stone' if solid_below else False
            is_left_wall = solid_left is not None and solid_left.tile_type.name == 'stone' if solid_left else False
            is_right_wall = solid_right is not None and solid_right.tile_type.name == 'stone' if solid_right else False


            # expand horizontally
            if (left or right) and not (above or below):
                next_x = x + 1
                while Vec2(next_x, y) in spike_tiles and Vec2(next_x, y) not in visited:
                    width += 1
                    visited.add(Vec2(next_x, y))
                    next_x += 1
                spikes.append(HSpike(tile.pos, width, is_ceiling))

            # expand vertically
            elif (above or below) and not (left or right):
                next_y = y + 1
                while Vec2(x, next_y) in spike_tiles and Vec2(x, next_y) not in visited:
                    height += 1
                    visited.add(Vec2(x, next_y))
                    next_y += 1
                spikes.append(VSpike(tile.pos, height, is_right_wall))

            else:
                spikes.append(CSpike(tile.pos, is_ceiling, is_floor, is_left_wall, is_right_wall))

        tilemap.remove_tiles(spike_tiles.values())
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