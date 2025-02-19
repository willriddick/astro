import os
import random
import pygame
from src.game.debug import Debug
from src.level_gen import CONFIGS, generate_level, Attribute
from src.util import Vec2, Direction
from src.tilemap import TileMap, Tile
from src.level_gen import LevelMap
import src.game.assets as assets

MAPS_PATH = 'assets/maps'

class Level:
    current: 'Level' = None

    def __init__(self, seed = None, config = CONFIGS[0], map_path: str = None):
        from .components import Entity, Collider
        from .player import Player 
        from src.game.entities import StarSpawner
        
        Level.current = self

        self.background_color = (24, 20, 37)

        self.entities: list[Entity] = []
        self.colliders: list[Collider] = []

        self.spawn_tile = None
        self.exit_tile = None
        self.spawn_pos = pygame.Vector2(16, 16)
        self.exit_pos = pygame.Vector2(0, 0)

        if map_path:
            self.tilemap = TileMap.load(map_path, assets.TILESET)
        else:
            self.tilemap = self.generate(config, seed)
        
        self.tilemap.create_border(assets.TILESET.get_by('stone'))

        if self.spawn_tile:
            self.spawn_pos = self.spawn_tile.pos
        if self.exit_tile:
            self.exit_pos = self.exit_tile.pos
        
        self.spikes = Level._create_spikes(self.tilemap)
        self.entities.extend(self.spikes)
        
        self.star_spawner = StarSpawner(invert_depth=True)
        self.star_spawner.spawn(50)
        
        self.player = Player()
        self.entities.append(self.player)
        self.player.spawn(self.spawn_pos)

        self.tilemap_surface = self.tilemap.get_surface()
    
    def update(self) -> None:
        for entity in self.entities:
            entity.update()
        
        self.star_spawner.update()
    
    def render(self, display: pygame.Surface, offset: pygame.Vector2) -> None:
        # background
        display.fill(self.background_color)

        # display stars
        self.star_spawner.render(display, offset)

        # display prerendered tilemap surface
        if self.tilemap_surface:
            display.blit(self.tilemap_surface, offset)
        
        # display all entities relative to the offset
        for entity in Level.current.entities:
            entity.render(display, offset)
        
        # debug display colliders 
        if Debug.enabled():
            for collider in Level.current.colliders:
                collider.render(display, offset)

    def register_collider(self, collider: 'Collider'):
        self.colliders.append(collider)

    def unregister_collider(self, collider: 'Collider'):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def get_colliders(self) -> list['Collider']:
        return self.colliders

    def generate(self, config: str, seed: int | str = None, room_size = Vec2(14, 10)) -> None:
        level_map: LevelMap = generate_level(config, seed)
        tilemap = TileMap(assets.TILESET, size=Vec2(0, 0))

        for y in range(level_map.config.rows):
            for x in range(level_map.config.cols):
                room = level_map.get_room_at(Vec2(x, y))

                # if room does not exit at postion (x, y) in level_map, fill 
                if room is None:
                    Level._fill_empty_room(tilemap, Vec2(x, y), room_size)
                    continue
                
                # if room exists at postion (x, y) in level_map
                sub, flip = self._get_folder_flip(room.key)
                map_folder = os.path.join(MAPS_PATH, sub)
                map_paths: list[str] = []
                for name in os.listdir(map_folder):
                    map_paths.append(os.path.join(map_folder, name))
                map_path = random.choice(map_paths)
                new_map = TileMap.load(map_path, assets.TILESET)

                if room.has_attribute(Attribute.ENTRANCE):
                    pos = random.choice(new_map.get_valid_floor(['stone'])).tile_pos
                    self.spawn_tile = new_map.create_tile(assets.TILESET.get_by('entrance'), 0, Vec2(pos.x, pos.y - 1))

                tilemap.place_tilemap(new_map, room.position, flip)
               
        return tilemap
    
    @staticmethod
    def _create_spikes(tilemap: TileMap) -> list['Spike']:
        """
        Queues for the spike tiles within a TileMap and creates Spike entities for each grouping
        based on three sets, horizontal, vertical, and corner tiles. This greatly reduces the 
        entity/collider count by creating a single entity for a grouping of spikes.
        """
        from src.game.entities import Spike, HSpike, VSpike, CSpike
        spikes: set[Spike] = set()
        horizontal_tiles: set[Tile] = set()
        vertical_tiles: set[Tile] = set()
        corner_tiles: set[Tile] = set()
        
        # categorize all spikes into three sets: horizontal, vertical, and corner
        spike_tiles = tilemap.get_tiles_with('spike')
        for tile in spike_tiles:
            a = []  # up, down, left, right
            w = []
            for direction in Direction.cardinals():
                adj = tilemap.get_tile(Vec2(tile.tile_pos.x, tile.tile_pos.y), direction)
                a.append(bool(adj and adj.tile_type.name == 'spike'))
                w.append(bool(adj and adj.tile_type.name == 'stone'))

            if any(a[2:]) and not any(a[:2]):    # row spike: left/right only
                horizontal_tiles.add(tile)
            elif any(a[:2]) and not any(a[2:]):  # column spike: up/down only
                vertical_tiles.add(tile)
            elif not any(a[2:]) and any(w[:2]):  # single spike: but stone above/below
                horizontal_tiles.add(tile)
            elif not any(a[:2]) and any(w[2:]):  # single spike: but stone left/right
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
    def _fill_empty_room(tilemap: TileMap, room_pos: Vec2, room_size: Vec2) -> None:
        tilemap.create_tile_rect(
            assets.TILESET.get_by('stone'), 
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