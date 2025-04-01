import pygame
from src.debug import DEBUG
from src.camera import CAMERA
from src.tilemap import TileMap
from src.level_gen import LevelMap
import src.graphics as graphics


class Level:

    def __init__(self):
        self.BACKGROUND_COLOR = graphics.PALETTE[15]
        self.star_spawner = None
        self.shooting_star = None

        self.level_map: LevelMap = None

        self.tilemap: TileMap = None
        self.spawn_tile = None
        self.spawn_pos = pygame.Vector2(0, 0)
        self.exit_tile = None
        self.exit_pos = pygame.Vector2(0, 0)

        from .components import Entity, Collider
        self.entities: list[Entity] = []
        self.colliders: list[Collider] = []
        self.rocket = None
        self.ghosts = []
    
    def start(self) -> None:
        pass

    def update(self) -> None:
        self.shooting_star.update()
        for entity in self.entities:
            entity.update()
        
    def render(self, display: pygame.Surface, offset: pygame.Vector2) -> None:
        # background
        display.fill(self.BACKGROUND_COLOR)

        # display stars
        self.star_spawner.render(display, offset)
        self.shooting_star.render(display, offset)

        # display prerendered tilemap surface
        if self.tilemap_surface:
            display.blit(self.tilemap_surface, offset)
        
        # display entities relative to the offset
        for entity in self.entities:
            if CAMERA.is_visible(entity.center):
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
