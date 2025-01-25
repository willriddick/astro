from typing import Callable
import pygame
from src.util import Vec2, draw_rect

class Collider:
    def __init__(self, level: 'Level', owner, size: Vec2, offset: Vec2):
        self.level = level
        self.level.register_collider(self)

        self.owner = owner
        self.size = size
        self.offset = offset
        self.enabled = True
        self.pos = pygame.Vector2(0, 0)
    
    @property
    def rect(self) -> pygame.FRect:
        return pygame.FRect(
            self.pos.x + self.offset.x,
            self.pos.y + self.offset.y,
            self.size.x,
            self.size.y
        )

    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)

    def get_overlap(self) -> list['Collider']:
        """Returns colliders overlapping with this collider."""
        if not self.enabled:
            return []

        return [
            collider for collider in self.level.colliders
            if collider != self and self.rect.colliderect(collider.rect)
        ]
   
    def get_nearest(self, filter_: Callable[['Collider'], bool]) -> 'Collider':
        """Returns the nearest collider that passes the filter."""
        if not self.enabled:
            return None

        nearest = None
        distance = 99999
        for collider in self.get_overlap():
            if not filter_(collider):
                continue

            new_distance = collider.center.distance_to(self.center)
            if new_distance < distance:
                nearest = collider
                distance = new_distance
            
        return nearest
    
    def update(self, pos: pygame.Vector2):
        self.pos = pos
   
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        draw_rect(
            display, 
            offset=offset, 
            rect=self.rect,
            outline_color=(255, 0, 255, 50),
        )
