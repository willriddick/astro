import random
import os
from src.level_gen import LevelBuilder, Attribute
from src.tilemap import TileMap, Tile 
from src.util import Assets, Vec2

class MapBuilder:
    @staticmethod
    def generate(config: str, seed: int | float | str = None) -> tuple[TileMap, Tile]:
        level = LevelBuilder.generate_level(config, seed)
        tilemap = TileMap(Assets.TILESET, size=Vec2(0, 0))

        for room in level.map.values():
            map_folder = f'maps/{room.key}' 
            map_paths: list[str] = []
            for name in os.listdir(map_folder):
                map_paths.append(map_folder + '/' + name)
            map_path = random.choice(map_paths)
            new_map = TileMap.load(map_path, Assets.TILESET)
            
            if room.has_attribute(Attribute.ENTRANCE):
                floors = new_map.get_valid_floor('stone')
                pos = random.choice(floors).tile_pos
                spawn_tile = new_map.create_tile(Assets.TILESET.get_by('door'), 0, Vec2(pos[0], pos[1] - 1))

            tilemap.place_tilemap(new_map, room.position, False)
        
        tilemap.spawn_tile = spawn_tile
        return tilemap
    