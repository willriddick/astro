import pygame
from .sprite import Sprite

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], rect_size: tuple[int, int]):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.rect_size = rect_size
        self.sprite: Sprite = None
    
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        assert self.sprite, 'Sprite not set {self}'
        self.sprite.render(display, offset)
    
    def set_pos(self, pos: pygame.Vector2):
        self.pos = pos
    
    def get_pos(self) -> pygame.Vector2:
        return self.pos
    
    def get_center(self) -> pygame.Vector2:
        return pygame.Vector2(self.get_rect().center)
    
    def get_rect(self):
        return pygame.FRect(self.pos.x, self.pos.y, self.rect_size[0], self.rect_size[1])
