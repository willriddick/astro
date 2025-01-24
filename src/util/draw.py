import pygame
from .vec2 import Vec2

def draw_rect(
        display: pygame.Surface,
        offset: pygame.Vector2 = None,
        pos = pygame.Vector2(0, 0),
        size = Vec2(0, 0),
        line_width = 1,
        outline_color = pygame.Color(0, 0, 0, 127),
        fill_color = pygame.Color(255, 255, 255, 127),
    ):
    surface = pygame.Surface((size.x, size.y), pygame.SRCALPHA)
    surface.fill(fill_color) 
    pygame.draw.rect(surface, outline_color, (0, 0, size.x, size.y), line_width)
    position = pygame.Vector2(pos.x + offset.x, pos.y + offset.y) if offset else pos
    display.blit(surface, position)
