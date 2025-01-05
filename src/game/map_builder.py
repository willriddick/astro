
import pygame
import random
import os
from src.level_gen import LevelBuilder, Level
from src.tilemap import TileMap, TileSet, Tile

class MapBuilder:
    @staticmethod
    def generate(tileset: TileSet, config: str, seed: int | float | str) -> Level:
        level = LevelBuilder.generate_level(config, seed)
        tilemap = TileMap(tileset, size=(0, 0), debug=False)

        for room in level.map.values():
            map_folder = f'maps/{room.key}' 
            map_paths: list[str] = []
            for name in os.listdir(map_folder):
                map_paths.append(map_folder + '/' + name)
            map_path = random.choice(map_paths)
            new_map = TileMap.load(map_path, tileset)
            tilemap.place(new_map, room.position, False)
        
        return tilemap
    
    @staticmethod
    def get_spawn_pos(tilemap: TileMap) -> pygame.Vector2:
        spawn_pos = (0, 0)
        doors = tilemap.get_tiles_with_type('door') 
        if doors:
            door: Tile = random.choice(doors)
            spawn_pos = door.pixel_pos
        return pygame.Vector2(spawn_pos)
       