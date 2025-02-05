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
        
        Level._merge_spikes(self.tilemap)
        
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
    def _merge_spikes(tilemap: TileMap) -> None:
        from .spike import Spike

        spikes = tilemap.get_tiles_with('spike')
        print(spikes)
        spikes.sort(key=lambda s: (s.pos.y, s.pos.x))
        new_spike = None
        prev = None

        for spike in spikes:  
            if new_spike is None:
                new_spike = Spike(spike.pos)

            if prev is None:
                prev = spike
                continue

            print(prev.pos, spike.pos)
            if (prev.pos.y == spike.pos.y 
                and prev.pos.x + 16 == spike.pos.x
            ):
                new_spike.update_width(new_spike.width + 1)
                print(new_spike.width)
            else:
                new_spike = Spike(spike.pos)
            
            prev = spike
            del spike
    
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
    def _fill_empty_room(tilemap: TileMap, pos: Vec2, room_size: Vec2) -> None:
        tilemap.create_tile_rect(
            Assets.TILESET.get_by('stone'), 
            pygame.Rect(pos.x * room_size.x, pos.y * room_size.y, room_size.x, room_size.y)
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