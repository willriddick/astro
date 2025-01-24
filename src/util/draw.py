import pygame
from .vec2 import Vec2

def draw_rect(
        display: pygame.Surface,
        offset: pygame.Vector2,
        rect: pygame.Rect,
        line_width = 1,
        fill_color = pygame.Color(255, 255, 255, 127),
        outline_color = pygame.Color(0, 0, 0, 127),
    ):
    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    surface.fill(fill_color) 
    pygame.draw.rect(surface, outline_color, (0, 0, rect.width, rect.height), line_width)
    position = pygame.Vector2(rect.x + offset.x, rect.y + offset.y) if offset else rect.topleft
    display.blit(surface, position)
