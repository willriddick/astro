import numpy as np
import pygame
from src.util import Vec2, randf
from .level import Level
from .clock import Clock

class Camera:
    def __init__(self, size: Vec2):
        self.size = size
        self.display = pygame.Surface(size)
        self.fill_color = (24, 20, 37)

        self.pos = pygame.Vector2(0, 0)
        self.offset = pygame.Vector2(0, 0)
        self.boundary: pygame.Rect | None = None
        self.follow = False

        self.screenshake_offset = pygame.Vector2(0, 0)
        self.screenshake_timer = 0
        self.screenshake_intensity = 0

        self.level: Level | None = None

    def update(self) -> None:
        """Update the camera and render the display surface."""
        # Clear display surface
        self.display.fill(self.fill_color)

        # Update screenshake effect
        self._handle_screenshake()

        # Calculate the offset from the in-game position
        self.offset = pygame.Vector2(
            self.pos.x - self.size.x // 2,
            self.pos.y - self.size.y // 2
        ) + self.screenshake_offset

        # Render the tilemap  
        self._render_tilemap(self.level.tilemap)

        # Render all entities relative to the offset
        for entity in self.level.entities:
            entity.render(self.display, -self.offset)
        
        #for collider in self.level.colliders:
        #   collider.render(self.display, -self.offset)

    @property
    def rect(self) -> pygame.Rect:
        """Get the camera's current rectangle in the game world."""
        return pygame.Rect(
            self.pos.x - self.size.x // 2,
            self.pos.y - self.size.y // 2,
            self.size.x, 
            self.size.y
        )
    
    def set_pos(self, target_pos: pygame.Vector2) -> None:
        """Set the camera's position to a target position."""
        self.pos = self._clamp(target_pos, self.size, self.boundary)
    
    def move_to(self, target_pos: pygame.Vector2, smoothing=0.2):
        """Smoothly interpolate towards the target position using an exponential decay approach."""
        cos_smoothing = (1 - np.cos(smoothing * np.pi)) / 2
        self.pos = self.pos * (1 - cos_smoothing) + target_pos * cos_smoothing
        self.pos = self._clamp(self.pos, self.size, self.boundary)
   
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
            self.screenshake_intensity * 0.9
        else:
            self.screenshake_offset = pygame.Vector2(0, 0)
    

    def _clamp(self, pos: pygame.Vector2, size: Vec2, boundary: pygame.Rect) -> pygame.Vector2:
        if not boundary:
            return pos
        h_width = size.x // 2
        h_height = size.y // 2
        return pygame.Vector2(
            max(boundary.left + h_width, min(int(pos.x), boundary.right - h_width)),
            max(boundary.top + h_height, min(int(pos.y), boundary.bottom - h_height))
        )
    
    def _render_tilemap(self, tilemap) -> None:
        if not tilemap:
            return

        tile_size = tilemap.tile_size
        x_start = int(-self.offset.x // tile_size.x)
        x_stop = int((self.offset.x + self.display.width) // tile_size.x + 1)
        y_start = int(-self.offset.y // tile_size.y)
        y_stop = int((self.offset.y + self.display.height) // tile_size.y + 1)
        for x in range(x_start, x_stop):
            for y in range(y_start, y_stop):
                tile = tilemap.get_tile(Vec2(x, y))
                if tile:
                    tile.render(self.display, self.offset)
    