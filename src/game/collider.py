import pygame
from src.util import Vec2, draw_rect

class Collider:
    def __init__(self, size: Vec2, offset: Vec2):
        self.size = size
        self.pos = pygame.Vector2(0, 0)
        self.offset = offset
        self.nearest: 'Collider' | None = None
        self.enabled = True
        self.debug = True
    
    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.pos.x + self.offset.x,
            self.pos.y + self.offset.y,
            self.size.x,
            self.size.y
        )

    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)
    
    def update(self, pos: pygame.Vector2, colliders: list['Collider']):
        self.pos = pos
        if self.enabled:
            self.nearest = self.get_nearest_collider(colliders)
        else:
            self.nearest = None
    
    def get_nearest_collider(self, colliders: list['Collider']) -> 'Collider':
        nearest = None
        distance = 99999
        for collider in self.get_colliders(colliders):
            new_distance = collider.center.distance_to(self.center)
            if new_distance < distance:
                nearest = collider
                distance = new_distance
        return nearest
    
    def get_colliders(self, colliders: list['Collider']) -> list['Collider']:
        return [collider for collider in colliders if self.rect.colliderect(collider.rect)]
    
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        alpha = 255 if self.nearest else 100
        draw_rect(
            display, offset, 
            pygame.Vector2(self.pos.x + self.offset.x, self.pos.y + self.offset.y),
            size=self.size, 
            outline_color=(255, 0, 255, alpha),
            fill_color=(0, 0, 0, 0),
        )
