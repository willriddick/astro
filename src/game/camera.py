import numpy as np
import pygame
from src.util import Assets, Vec2, randf, draw_rect
from src.tilemap import TileMap
from .level import Level
from .clock import Clock
from .debug import Debug

class Camera:
    FILL_COLOR = (24, 20, 37)

    def __init__(self, size: Vec2):
        self.size = size
        self.display = pygame.Surface(size)

        self.offset = pygame.Vector2(0, 0)
        self.pos = pygame.Vector2(0, 0)
        self.smoothing = 0.0
        self.boundary: pygame.Rect | None = None

        self.screenshake_offset = pygame.Vector2(0, 0)
        self.screenshake_timer = 0
        self.screenshake_intensity = 0

        self.tilemap_surface = None

    def update(self) -> None:
        """Update the camera and render the display surface."""
        # Clear display surface
        self.display.fill(Camera.FILL_COLOR)

        # Update screenshake effect
        self._handle_screenshake()

        # Calculate the offset from the in-game position
        self.offset = pygame.Vector2(
            round(self.clamp_pos.x - self.size.x // 2 + self.screenshake_offset.x),
            round(self.clamp_pos.y - self.size.y // 2 + self.screenshake_offset.y)
        )

        # Render stars
        Level.current.star_spawner.render(self.display, -self.offset)

        # Render prerendered tilemap surface
        if self.tilemap_surface:
            self.display.blit(self.tilemap_surface, -self.offset)
    
        # Render debug display information
        if Debug.enabled():
            self._debug_display()

        # Render all entities relative to the offset
        for entity in Level.current.entities:
            entity.render(self.display, -self.offset)

        # Render debug shapes like colliders
        if Debug.enabled():
            for collider in Level.current.colliders:
                collider.render(self.display, -self.offset)
    
    def set_level(self, level: Level) -> None:
        """Set the current level and update the camera's tilemap surface."""
        self.tilemap_surface = self._render_tilemap(level.tilemap)
        self.boundary = level.tilemap.rect
        self.set_pos(level.spawn_pos)
   
    def _debug_display(self):
        text_surf = Assets.FONT.render(str(Debug.display()), antialias=False, color=(255, 255, 255))
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
        clamped_x = max(self.boundary.left + h_width, min(self.pos.x, self.boundary.right - h_width))
        clamped_y = max(self.boundary.top + h_height, min(self.pos.y, self.boundary.bottom - h_height))
        
        return pygame.Vector2(clamped_x, clamped_y)
    
    def set_pos(self, target_pos: pygame.Vector2) -> None:
        """Set the camera's position to a target position."""
        self.pos = target_pos
    
    def move_to(self, target_pos: pygame.Vector2, smoothing=10, factor=20) -> None:
        """Smoothly interpolate towards the target position using an exponential decay approach."""
        # Calculate dynamic smoothing based on the distance to the target
        distance_to_target = (target_pos - self.pos).length()
        dynamic_smoothing = smoothing * (1 + distance_to_target / factor) 
        
        # Apply exponential smoothing (cosine interpolation)
        self.smoothing = (1 - np.cos(dynamic_smoothing * np.pi * Clock.dt())) / 2
        
        # Clamp the position and update
        self.pos = self.pos * (1 - self.smoothing) + target_pos * self.smoothing
   
    def screenshake(self, duration: int, intensity: int) -> None:
        self.screenshake_timer = duration
        self.screenshake_intensity = intensity
    
    def _handle_screenshake(self) -> None:
        self.screenshake_timer = max(0, self.screenshake_timer - 1)
        if self.screenshake_timer > 0:
            self.screenshake_offset = pygame.Vector2(
                randf(-self.screenshake_intensity, self.screenshake_intensity, 0.1),
                randf(-self.screenshake_intensity, self.screenshake_intensity, 0.1),
            )
            self.screenshake_intensity *= 0.9
        else:
            self.screenshake_offset = pygame.Vector2(0, 0)
    
    def _render_tilemap(self, tilemap: TileMap) -> pygame.Surface:

        # create a transparent surface the size of our tilemap
        surface = pygame.Surface(
            (tilemap.size.x * tilemap.tile_size.x, tilemap.size.y * tilemap.tile_size.y),
            pygame.SRCALPHA 
        )
        surface.fill((0, 0, 0, 0))

        # render all tiles to the surface
        for tile in tilemap.map.values():
            if tile:
                tile.render(surface, pygame.Vector2(0, 0))
        
        # return prerendered tilemap surface
        return surface
    