import pygame
from src.util import Assets
from src.tilemap import TileMap
from .map_builder import generate
from .spike import Spike
from .gravity import Gravity
from .components import Collider, Entity

class Level:
    def __init__(self, 
        config = 'configs/0.json', 
        seed=None, 
        map_path: str = None
    ):
        if map_path:
            self.tilemap = TileMap.load(map_path, Assets.TILESET)
            self.spawn_tile = None
        else:
            self.tilemap, self.spawn_tile = generate(config, seed)
        
        self.spawn_pos = pygame.Vector2(32, 16)
        if self.spawn_tile:
            self.spawn_pos = pygame.Vector2(self.spawn_tile.pos)

        self.colliders: list[Collider] = []
        self.entities: list[Entity] = []

        for spike in self.tilemap.get_tiles_with('spike'):
            Spike(self, spike.pos)
            del spike
        
        for gravity in self.tilemap.get_tiles_with('gravity'):
            Gravity(self, gravity.pos)

    def register_collider(self, collider: 'Collider'):
        self.colliders.append(collider)

    def unregister_collider(self, collider: 'Collider'):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def get_colliders(self) -> list['Collider']:
        return self.colliders
