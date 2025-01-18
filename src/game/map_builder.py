import random
import os
from src.level_gen import generate_level, Attribute
from src.tilemap import TileMap, Tile 
from src.util import Assets, Vec2

class MapBuilder:
    @staticmethod
    def generate(config: str, seed: int | float | str = None) -> tuple[TileMap, Tile]:
        level = generate_level(config, seed)
        tilemap = TileMap(Assets.TILESET, size=Vec2(0, 0))
        size = "10x8"

        for room in level.map.values():
            sub, flip = MapBuilder.get_folder_flip(room.key)
            map_folder = f'maps/{size}/{sub}'
            map_paths: list[str] = []
            for name in os.listdir(map_folder):
                map_paths.append(map_folder + '/' + name)

            map_path = random.choice(map_paths)
            new_map = TileMap.load(map_path, Assets.TILESET)
            
            if room.has_attribute(Attribute.ENTRANCE):
                floors = new_map.get_valid_floor('stone')
                pos = random.choice(floors).tile_pos
                spawn_tile = new_map.create_tile(Assets.TILESET.get_by('door'), 0, Vec2(pos[0], pos[1] - 1))

            tilemap.place_tilemap(new_map, room.position, flip)
        
        tilemap.spawn_tile = spawn_tile
        return tilemap
    
    @staticmethod
    def get_folder_flip(key: int) -> tuple[str, bool]:
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