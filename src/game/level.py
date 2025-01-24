import pygame
from src.util import Assets
from src.tilemap import TileMap
from .player import Player
from .map_builder import generate
from .entity import Entity
from .spike import Spike
from .components import Collider, DamageComponent

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
        
        self.spawn_pos = pygame.Vector2(32, 32)
        if self.spawn_tile:
            self.spawn_pos = pygame.Vector2(self.spawn_tile.pos)

        self.colliders: list[Collider] = []
        self.entities: list[Entity] = []

        for spike in self.tilemap.get_tiles_with('spike'):
            Spike(self, spike.pos)
            del spike

    def register_collider(self, collider: 'Collider'):
        self.colliders.append(collider)

    def unregister_collider(self, collider: 'Collider'):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def get_colliders(self) -> list['Collider']:
        return self.colliders
