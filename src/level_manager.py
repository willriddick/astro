import random 
import os
import pygame
from src.level_gen import CONFIGS
from src.camera import CAMERA
from src.level_gen import generate_level, Attribute
from src.level import Level
from src.util import Vec2, Direction
from src.tilemap import TileMap, Tile
from src.tilemap import TileMap
import src.graphics as graphics


MAPS_PATH = os.path.join('assets', 'maps')
STAR_COUNT = 100


class LevelManager:
    def __init__(self):
        self.player = None
        self.current = None
    
    def new_level(self, seed: int = None, config_index=0, map_path: str = None):
        """Create a new level with the given seed and map path."""
        if seed:
            random.seed(seed)

        self.current = level = Level()
        
        if map_path:
            level.tilemap = TileMap.load(map_path, graphics.TILESET)
        else:
            level.tilemap = LevelManager._generate(level, CONFIGS[config_index])

        level.tilemap.create_border(graphics.TILESET.get_by('stone'))
        
        if level.spawn_tile:
            level.spawn_pos = level.spawn_tile.pos
            level.tilemap.remove_tile(level.spawn_tile.tile_pos)    
        
        from src.entities import Rocket, FuelCell

        if level.exit_tile:
            level.exit_pos = level.exit_tile.pos
            level.rocket = Rocket(level.exit_tile.pos) 
            level.rocket.spawn()
            level.entities.append(level.rocket)
            level.tilemap.remove_tile(level.exit_tile.tile_pos)    
        
        for fuel_cell in level.fuel_cell_tiles:
            new_cell = FuelCell(fuel_cell.pos)
            level.fuel_cells.append(new_cell)
            level.entities.append(new_cell)
            new_cell.spawn()
            level.tilemap.remove_tile(fuel_cell.tile_pos)
            
        # spawn spikes
        spikes = LevelManager._create_spikes(level.tilemap)
        level.entities.extend(spikes)

        # spawn stars
        from src.entities import StarSpawner, ShootingStar
        level.star_spawner = StarSpawner(invert_depth=True)
        level.star_spawner.spawn(STAR_COUNT)
        level.shooting_star = ShootingStar()
        
        # spawn player
        from src.player import Player
        if self.player is None:
            self.player = Player()

        level.entities.append(self.player)
        self.player.spawn(level.spawn_pos)

        level.tilemap_surface = level.tilemap.get_surface()

        CAMERA.set_pos(level.spawn_pos)
        CAMERA.set_boundary(level.tilemap.rect)
        level.start()
    

    @staticmethod
    def _generate(level: Level, config: str, room_size = Vec2(14, 10)) -> None:
        level.tilemap = TileMap(graphics.TILESET, size=Vec2(0, 0))
        level.level_map = generate_level(config)

        entrance_tile = graphics.TILESET.get_by('entrance')
        exit_tile = graphics.TILESET.get_by('exit')
        collectable_tile = graphics.TILESET.get_by('collectable')

        for y in range(level.level_map.config.rows):
            for x in range(level.level_map.config.cols):
                room = level.level_map.get_room_at(Vec2(x, y))

                # if room does not exit at postion (x, y) in level_map, fill 
                if room is None:
                    LevelManager._fill_empty_room(level.tilemap, Vec2(x, y), room_size)
                    continue
                
                # if room exists at postion (x, y) in level_map
                sub, flip = LevelManager._get_folder_flip(room.key)
                map_folder = os.path.join(MAPS_PATH, sub)
                map_paths: list[str] = []

                # sort the map folder for random reproducibility
                for name in sorted(os.listdir(map_folder)):
                    map_paths.append(os.path.join(map_folder, name))

                # choose a random map from the folder and load it
                map_path = random.choice(sorted(map_paths))
                new_map = TileMap.load(map_path, graphics.TILESET)

                if room.has_attribute(Attribute.ENTRANCE):
                    pos = random.choice(new_map.get_valid_floor()).tile_pos
                    level.spawn_tile = new_map.create_tile(entrance_tile, 0, Vec2(pos.x, pos.y - 1))
                
                if room.has_attribute(Attribute.EXIT):
                    pos = random.choice(new_map.get_valid_floor()).tile_pos
                    level.exit_tile = new_map.create_tile(exit_tile, 0, Vec2(pos.x, pos.y - 1))
                
                if room.has_attribute(Attribute.COLLECTABLE):
                    pos = random.choice(new_map.get_empty_positions())
                    level.fuel_cell_tiles.append(new_map.create_tile(collectable_tile, 0, Vec2(pos.x, pos.y)))

                level.tilemap.place_tilemap(new_map, room.position, flip)
               
        return level.tilemap
    

    @staticmethod
    def _create_spikes(tilemap: TileMap) -> list['Spike']:
        """
        Queues for the spike tiles within a TileMap and creates Spike entities for each grouping
        based on three sets, horizontal, vertical, and corner tiles. This greatly reduces the 
        entity/collider count by creating a single entity for a grouping of spikes.
        """
        from src.entities import Spike, HSpike, VSpike, CSpike
        spikes: set[Spike] = set()
        horizontal_tiles: set[Tile] = set()
        vertical_tiles: set[Tile] = set()
        corner_tiles: set[Tile] = set()
        
        # categorize all spikes into three sets: horizontal, vertical, and corner
        spike_tiles = tilemap.get_tiles_with('spike')
        tile_wall_map = {}

        for tile in spike_tiles:
            s = []  # spikes: up, down, left, right
            w = []  # walls:  up, down, left, right 
            for _, direction in enumerate(Direction.cardinals()):
                adj = tilemap.get_tile(Vec2(tile.tile_pos.x, tile.tile_pos.y), direction)
                s.append(bool(adj and adj.tile_type.name == 'spike'))
                w.append(bool(adj and adj.tile_type.collision and adj.tile_type.name != 'platform'))
            
            tile_wall_map[tile] = w  # store walls for later use

            if any(s[2:]) and not any(s[:2]):    # row spike: left/right only
                horizontal_tiles.add(tile)
            elif any(s[:2]) and not any(s[2:]):  # column spike: up/down only
                vertical_tiles.add(tile)
            elif not any(s[2:]) and any(w[:2]):  # single spike: but stone above/below
                horizontal_tiles.add(tile)
            elif not any(s[:2]) and any(w[2:]):  # single spike: but stone left/right
                vertical_tiles.add(tile)
            else:                                # must be a corner spike
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
            
            above = tile_wall_map[tile][0]
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
            
            right = tile_wall_map[tile][3]
            spikes.add(VSpike(tile.pos, height, right))

        # create spike entities for corner set
        for tile in corner_tiles:
            w = tile_wall_map[tile]  # reuse stored walls
            spikes.add(CSpike(tile.pos, w[0], w[3]))  # above, right

        # remove tile object from tilemap now that we have created an entity
        tilemap.remove_tiles(spike_tiles)
        return spikes
        

    @staticmethod
    def _fill_empty_room(tilemap: TileMap, room_pos: Vec2, room_size: Vec2) -> None:
        tilemap.create_tile_rect(
            graphics.TILESET.get_by('stone'), 
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


LEVEL_MANAGER = LevelManager()
