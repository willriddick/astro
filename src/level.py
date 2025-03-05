import pygame
from src.debug import DEBUG
from src.tilemap import TileMap
from src.level_gen import LevelMap


class Level:

    def __init__(self):
        self.background_color = (24, 20, 37)
        self.star_spawner = None

        self.level_map: LevelMap = None

        self.tilemap: TileMap = None
        self.spawn_tile = None
        self.spawn_pos = pygame.Vector2(16, 16)

        from .components import Entity, Collider
        self.entities: list[Entity] = []
        self.colliders: list[Collider] = []
        self.ghosts = []
    
    def start(self) -> None:
        print('Level started')

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
        for entity in self.entities:
            entity.render(display, offset)
        
        # debug display colliders 
        if DEBUG.enabled:
            for collider in self.colliders:
                collider.render(display, offset)
    
    def register_collider(self, collider: 'Collider'):
        self.colliders.append(collider)

    def unregister_collider(self, collider: 'Collider'):
        if collider in self.colliders:
            self.colliders.remove(collider)

    def get_colliders(self) -> list['Collider']:
        return self.colliders
