from typing import Callable
import pygame
from src.util import Vec2, draw_rect
from src.game.level import Level

class Collider:
    def __init__(self, size: Vec2, offset: Vec2):
        self.owners: set[object] = set()
        Level.current.register_collider(self)
        self.size = size
        self.offset = offset
        self.layer = 0
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
    
    def add_owner(self, owner: object):
        self.owners.add(owner)
    
    def get_owner(self, type_: type) -> object:
        for owner in self.owners:
            if isinstance(owner, type_):
                return owner
        return None
    
    def has_owner(self, type_: type) -> bool:
        return self.get_owner(type_)
    
    def get_nearest(self, type: type) -> object:
        """Returns the object of the given type that is nearest to this collider."""
        if not self.enabled:
            return None

        nearest = None
        distance = 99999
        for collider in self._get_overlap(lambda c: c.has_owner(type)):
            new_distance = collider.center.distance_to(self.center)
            if new_distance < distance:
                nearest = collider.get_owner(type)
                distance = new_distance
            
        return nearest
    
    def _get_overlap(self, filter_: Callable[['Collider'], bool] = lambda _: True) -> list['Collider']:
        """
        Returns overlapping that pass the filter. If this collider is not enabled, an empty list is returned.

        Args:
            filter_: A function that accepts a Collider and returns a boolean. 

        Returns:
            A list of colliders that overlap with this collider and pass the filter.
        """
        if not self.enabled:
            return []

        return [
            collider for collider in Level.current.colliders
            if collider.enabled
                and collider is not self
                and self.rect.colliderect(collider.rect)
                and filter_(collider)
        ]
   
    def update(self, pos: pygame.Vector2):
        self.pos = pos
   
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        draw_rect(
            display=display, 
            offset=offset, 
            rect=self.rect,
            outline_color=(255, 0, 255, 100),
        )
