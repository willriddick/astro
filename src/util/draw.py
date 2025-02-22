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
