import pygame


def draw_rect(
        display: pygame.Surface,
        offset = pygame.Vector2(0, 0),
        rect = pygame.Rect(0, 0, 0, 0),
        fill_color = pygame.Color(0, 0, 0, 0),
        outline_color = pygame.Color(0, 0, 0, 0),
        line_width = 1,
    ):
    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    surface.fill(fill_color) 
    pygame.draw.rect(surface, outline_color, (0, 0, rect.width, rect.height), line_width)
    position = pygame.Vector2(rect.topleft) + offset
    display.blit(surface, position)

def draw_circle(
        display: pygame.Surface,
        offset = pygame.Vector2(0, 0),
        center = pygame.Vector2(0, 0),
        radius = 0,
        fill_color = pygame.Color(0, 0, 0, 0),
        outline_color = pygame.Color(0, 0, 0, 0),
        line_width = 1,
    ):
    surface_size = radius * 2
    surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
    pygame.draw.circle(surface, fill_color, (radius, radius), radius)
    if line_width > 0:
        pygame.draw.circle(surface, outline_color, (radius, radius), radius, line_width)
    position = pygame.Vector2(center) - pygame.Vector2(radius, radius) + offset
    display.blit(surface, position)
