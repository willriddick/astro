import pygame
from src.util.assets import Assets, Vec2

class Button():

    SURFACE_SIZE = Vec2(224, 16)
    X_OFFSET = 5
    OFFSET_SPEED = 0.05 

    def __init__(self, text: str, callback: callable):
        self.text = text
        self.callback = callback
        self.hovered = False
        self.x_offset = 0
        self.target_offset = 0 

        self.HOVERED_COLOR = Assets.PALETTE[34]
        self.DEFAULT_COLOR = Assets.PALETTE[5]
    
    def __str__(self):
        return self.text
   
    def select(self):
        self.callback()
    
    def update(self, hovered: bool):
        self.hovered = hovered
        self.target_offset = self.X_OFFSET if self.hovered else 0
        self.x_offset += (self.target_offset - self.x_offset) * self.OFFSET_SPEED
    
    def get_surface(self) -> pygame.Surface:
        color = self.HOVERED_COLOR if self.hovered else self.DEFAULT_COLOR
        surface = pygame.Surface(self.SURFACE_SIZE, pygame.SRCALPHA)
        surface.blit(Assets.FONT.render(self.text, antialias=False, color=color), (self.x_offset, 0))
        return surface
