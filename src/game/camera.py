import numpy as np
import pygame
from typing import Callable
from src.util import Vec2, randf, draw_rect, Timer
from .level import Level
from .clock import Clock
from .debug import Debug
import src.game.assets as assets

class Camera:

    DISTANCE_BUFFER = 7

    def __init__(self, size: Vec2):
        self.size = size
        self.display = pygame.Surface(size)

        self.offset = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(0, 0)
        self.smoothing = 0.0
        self.boundary: pygame.Rect = None

        self.screenshake_offset = pygame.Vector2(0, 0)
        self.screenshake_timer = Timer()
        self.screenshake_intensity = 0

        self.render_callback: Callable[[pygame.Surface, pygame.Vector2], None] = None

    def update(self) -> None:
        """Update the camera and render the display surface."""
        # clear display surface
        self.display.fill((0, 0, 0))

        # update screenshake effect
        self._handle_screenshake()

        # calculate the offset from the in-game position
        self.offset = pygame.Vector2(
            round(self.clamp_pos.x - self.size.x // 2),
            round(self.clamp_pos.y - self.size.y // 2)
        ) + self.screenshake_offset

        # render the callback
        self.render_callback(self.display, -self.offset)

        # render debug display
        if Debug.enabled():
            self._debug_display()
    
    def set_render_callback(self, callback: Callable[[pygame.Surface, pygame.Vector2], None]):
        """Set a new render function for the camera."""
        self.render_callback = callback
    
    def _debug_display(self):
        # display debug information
        text_surf = assets.FONT.render(str(Debug.display()), antialias=False, color=(255, 255, 255))
        text_surf.set_alpha(70)
        text_rect = text_surf.get_rect()
        draw_rect(
            self.display,
            rect=pygame.Rect(0, 0, 100, text_rect.height + 8),
            fill_color=(0, 0, 0, 40),
            outline_color=(0, 0, 0, 0)
        )
        self.display.blit(text_surf, (4, 4))

    @property
    def debug(self) -> str:
        return (
            f'x:{int(self.pos.x):4} y:{int(self.pos.y):4}\n'
            f'clamp x:{int(self.clamp_pos.x):4} y:{int(self.clamp_pos.y):4}\n'
            f'smoothing: {self.smoothing:.3f}\n'
        )

    @property
    def rect(self) -> pygame.Rect:
        """Get the camera's current rectangle in the game world."""
        return pygame.Rect(
            self.clamp_pos.x - self.size.x // 2,
            self.clamp_pos.y - self.size.y // 2,
            self.size.x, 
            self.size.y
        )
    
    @property
    def clamp_pos(self) -> pygame.Vector2:
        if not self.boundary:
            return self.pos
        
        # Half the width and height of the boundary (use float division for precision)
        h_width = self.size.x / 2
        h_height = self.size.y / 2

        # Ensure the position stays within the clamped bounds
        boundary = Level.current.tilemap.rect
        clamped_x = max(boundary.left + h_width, min(self.pos.x, boundary.right - h_width))
        clamped_y = max(boundary.top + h_height, min(self.pos.y, boundary.bottom - h_height))
        
        return pygame.Vector2(clamped_x, clamped_y)
    
    def set_pos(self, target_pos: pygame.Vector2):
        """Set the camera's position to a target position."""
        self.pos = target_pos
    
    def move_to(self, target_pos: pygame.Vector2, smoothing=10, factor=20):
        """Smoothly interpolate towards the target position using an exponential decay approach."""
        # Calculate dynamic smoothing based on the distance to the target
        distance_to_target = (target_pos - self.pos).length()

        if distance_to_target < self.DISTANCE_BUFFER:
            return

        dynamic_smoothing = smoothing * (1 + distance_to_target / factor) 
        
        # Apply exponential smoothing (cosine interpolation)
        self.smoothing = (1 - np.cos(dynamic_smoothing * np.pi * Clock.dt())) / 2
        
        # Clamp the position and update
        self.pos = self.pos * (1 - self.smoothing) + target_pos * self.smoothing

    def screenshake(self, duration: int, intensity: int):
        self.screenshake_timer.start(duration)
        self.screenshake_intensity = intensity
    
    def _handle_screenshake(self):
        if self.screenshake_timer.is_active:
            self.screenshake_offset = pygame.Vector2(
                randf(-self.screenshake_intensity, self.screenshake_intensity, 0.1),
                randf(-self.screenshake_intensity, self.screenshake_intensity, 0.1),
            )
            self.screenshake_intensity *= 0.9
        else:
            self.screenshake_offset = pygame.Vector2(0, 0)
    
    def get_blank(self) -> pygame.Surface:
        return pygame.Surface(self.size)
    