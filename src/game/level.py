import pygame
from src.util import Assets, Vec2
from src.tilemap import TileMap
from src.game.collider import Collider
from src.game.damage import DamageComponent
from src.game.player import Player
from src.game.map_builder import generate
from src.game.entity import Entity

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

        if self.spawn_tile:
            self.spawn_pos = pygame.Vector2(self.spawn_tile.pixel_pos)
        else:
            self.spawn_pos = pygame.Vector2(32, 32)

        self.colliders: list[Collider] = []
        self.entities: list[Entity] = []

        damage_test = DamageComponent()
        test_collider = Collider(damage_test, Vec2(16, 16), Vec2(0, 0))
        damage_test.collider = test_collider
        damage_test.update(pygame.Vector2(32, 32))
        self.register_collider(test_collider)

    def register_collider(self, collider: 'Collider'):
        self.colliders.append(collider)

    def unregister_collider(self, collider: 'Collider'):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def get_colliders(self) -> list['Collider']:
        return self.colliders
