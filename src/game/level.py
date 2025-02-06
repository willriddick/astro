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
        from .spike import Spike
        spikes: list[Spike] = []

        spike_tiles = sorted(tilemap.get_tiles_with('spike'), key=lambda s: (s.pos.y, s.pos.x))
        visited = set()

        for start_tile in spike_tiles:
            if start_tile.tile_pos in visited:
                continue  # skip already processed tiles

            above, below = False, False
                
            start_pos = start_tile.pos
            if above_tile := tilemap.get_tile(Vec2(start_pos.x, start_pos.y - 1)):
                if above_tile.tile_type.name == 'stone':
                    above = True

            if below_tile := tilemap.get_tile(Vec2(start_pos.x, start_pos.y + 1)):
                if below_tile.tile_type.name == 'stone':
                    below = True

            width, height = 1, 1
            visited.add(start_tile.tile_pos)

            # horizontal
            next_x = start_tile.tile_pos.x + 1
            while (
                (next_tile := tilemap.get_tile(Vec2(next_x, start_tile.tile_pos.y))) and
                next_tile.tile_type.name == 'spike' and
                next_tile.tile_pos not in visited
            ):
                width += 1
                next_x += 1
                visited.add(next_tile.tile_pos)
            
            """
            # verticle
            next_y = start_tile.tile_pos.y + 1
            while (
                (next_tile := tilemap.get_tile(Vec2(start_tile.tile_pos.x, next_y))) and
                next_tile.tile_type.name == 'spike' and
                next_tile.tile_pos not in visited
            ):
                height += 1
                visited.add(next_tile.tile_pos)
                visited_vertically.add(next_tile.tile_pos)
                next_y += 1
            """

            spikes.append(Spike(start_pos, width=width, height=height, above=above, below=below))

        tilemap.remove_tiles(spike_tiles )

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