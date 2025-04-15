import pygame
from src.util import Vec2
from src.clock import CLOCK
from src.constants import DISPLAY_WIDTH
from src.settings import SETTINGS
import src.graphics as graphics


TOP_BUFFER = 4
SCREEN_BUFFER = 8


class UI:
    def __init__(self):
        self.duration = 0.0
        self.collected = 0
        self.level = 1

        self.fuel_icon = graphics.FUEL_CELL
        self.fuel_icon_width = self.fuel_icon.get_width()
    
    def reset(self):
        self.duration = 0.0
        self.collected = 0
        self.level = 1

    def update(self, collected: int, fuel_cells: int, level):
        self.duration += CLOCK.dt
        self.collected = collected
        self.fuel_cells = fuel_cells
        self.level = level

    def render(self, display, offset):
        ui_surface = pygame.Surface((DISPLAY_WIDTH, 16), pygame.SRCALPHA)

        timer_text = f'{self.duration:0.2f}'
        timer_surf = graphics.FONT.render(timer_text, antialias=False, color=(255, 255, 255))
        timer_pos = Vec2(DISPLAY_WIDTH // 2 - timer_surf.get_width() // 2, TOP_BUFFER)
        ui_surface.blit(timer_surf, timer_pos)

        fuel_text = f'{self.collected}/{self.fuel_cells}'
        fuel_surf = graphics.FONT.render(fuel_text, antialias=False, color=(255, 255, 255))
        fuel_pos = Vec2(DISPLAY_WIDTH - SCREEN_BUFFER - self.fuel_icon_width - 16, TOP_BUFFER)
        ui_surface.blit(fuel_surf, fuel_pos)

        self.fuel_icon.set_colorkey((0, 0, 0))
        ui_surface.blit(self.fuel_icon, Vec2(DISPLAY_WIDTH - SCREEN_BUFFER - self.fuel_icon_width, TOP_BUFFER - 5))

        level_text = f'level: {self.level}'
        level_surf = graphics.FONT.render(level_text, antialias=False, color=(255, 255, 255))
        level_pos = Vec2(SCREEN_BUFFER + 4, TOP_BUFFER)
        ui_surface.blit(level_surf, level_pos)

        alpha = 255 * (SETTINGS.get('ui_alpha') / 10)
        ui_surface.set_alpha(alpha)

        display.blit(ui_surface, (0, 0))
