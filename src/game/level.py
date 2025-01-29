import os
import random
import pygame
from src.level_gen import CONFIGS, generate_level, Attribute
from src.util import Assets, Vec2
from src.tilemap import TileMap, Tile
from .player import Player 
from .components import Collider, Entity
from .spike import Spike
from .gravity import Gravity
from .exit import Exit

class Level:
    def __init__(self, seed = None, config = CONFIGS[0], map_path: str = None):
        self.camera = None
        self.entities: list[Entity] = []
        self.colliders: list[Collider] = []

        self.spawn_pos = pygame.Vector2(16, 16)
        self.exit_pos = pygame.Vector2(0, 0)

        if map_path:
            self.tilemap = TileMap.load(map_path, Assets.TILESET)
        else:
            self.tilemap = self.generate(config, seed)
        
        for spike in self.tilemap.get_tiles_with('spike'):
            Spike(self, spike.pos)
            del spike
        
        for gravity in self.tilemap.get_tiles_with('gravity'):
            Gravity(self, gravity.pos)
        
        self.player = Player(self, self.camera)
        self.entities.append(self.player)
        self.player.spawn(self.spawn_pos)

    def register_collider(self, collider: 'Collider'):
        self.colliders.append(collider)

    def unregister_collider(self, collider: 'Collider'):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def get_colliders(self) -> list['Collider']:
        return self.colliders

    def generate(self, config: str, seed  = None) -> None:
        level = generate_level(config, seed)
        tilemap = TileMap(Assets.TILESET, size=Vec2(0, 0))
        size = "14x10"

        for room in level.map.values():
            sub, flip = self._get_folder_flip(room.key)
            map_folder = f'assets/maps/{size}/{sub}'
            map_paths: list[str] = []
            for name in os.listdir(map_folder):
                map_paths.append(map_folder + '/' + name)

            map_path = random.choice(map_paths)
            new_map = TileMap.load(map_path, Assets.TILESET)
            
            if room.has_attribute(Attribute.ENTRANCE):
                pos = random.choice(new_map.get_valid_floor(['stone'])).tile_pos
                spawn_tile = new_map.create_tile(Assets.TILESET.get_by('entrance'), 0, Vec2(pos.x, pos.y - 1))
            
            if room.has_attribute(Attribute.EXIT):
                pos = random.choice(new_map.get_valid_floor(['stone'])).tile_pos
                exit_tile = new_map.create_tile(Assets.TILESET.get_by('exit'), 0, Vec2(pos.x, pos.y - 1))

            tilemap.place_tilemap(new_map, room.position, flip)
        
        self.spawn_pos = spawn_tile.pos
        self.exit_pos = exit_tile.pos
        Exit(self, self.exit_pos)

        return tilemap

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