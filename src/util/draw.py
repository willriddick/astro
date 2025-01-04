import pygame

def draw_transparent_rect(screen: pygame.Surface, rect: pygame.Rect, color: pygame.Color, alpha: int):
    transparent_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    transparent_surface.fill((*color, alpha))
    screen.blit(transparent_surface, (rect.x, rect.y))