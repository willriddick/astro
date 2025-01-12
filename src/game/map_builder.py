
import pygame
import random
import os
from src.level_gen import LevelBuilder, Level, Attribute
from src.tilemap import TileMap, Tile 
from src.util import Assets

class MapBuilder:
    @staticmethod
    def generate(config: str, seed: int | float | str = None) -> tuple[TileMap, Tile]:
        level = LevelBuilder.generate_level(config, seed)
        tilemap = TileMap(Assets.TILESET, size=(0, 0), debug=False)

        for room in level.map.values():
            map_folder = f'maps/{room.key}' 
            map_paths: list[str] = []
            for name in os.listdir(map_folder):
                map_paths.append(map_folder + '/' + name)
            map_path = random.choice(map_paths)
            new_map = TileMap.load(map_path, Assets.TILESET)
            
            if room.has_attribute(Attribute.ENTRANCE):
                pos = random.choice(new_map.get_valid_floor('stone')).tile_pos
                spawn_tile = new_map.create_tile(Assets.TILESET.get_by_name('door'), 0, (pos[0], pos[1] - 1))

            tilemap.place(new_map, room.position, False)
        
        return tilemap, spawn_tile
    