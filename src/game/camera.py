import numpy as np
import pygame
from src.game.level import Level
from src.util import Vec2, randf

class Camera:
    def __init__(self, size: Vec2):
        self.size = size
        self.display = pygame.Surface(size)
        self.fill_color = (24, 20, 37)

        self.pos = pygame.Vector2(0, 0)
        self.offset = pygame.Vector2(0, 0)
        self.boundary: pygame.Rect | None = None

        self.screenshake_offset = pygame.Vector2(0, 0)
        self.screenshake_timer = 0
        self.screenshake_intensity = 0
        self.screenshake_step = 0

        self.level: Level | None = None
    
    def update(self):
        """Update the camera and render the display surface."""
        # Clear display surface
        self.display.fill(self.fill_color)

        # Update screenshake effect
        self.handle_screenshake()

        # Calculate the offset from the in-game position
        self.offset = pygame.Vector2(
            self.pos.x - self.size.x // 2,
            self.pos.y - self.size.y // 2
        ) + self.screenshake_offset

        # Render the tilemap  
        self.render_tilemap(self.level.tilemap)

        # Render all entities relative to the offset
        for entity in self.level.entities:
            entity.render(self.display, -self.offset)
        
        # Render all colliders
        #for collider in self.level.colliders:
        #    collider.render(self.display, -self.offset)

    def render_tilemap(self, tilemap):
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
    
    def screenshake(self, duration: int, intensity: int):
        self.screenshake_timer = duration
        self.screenshake_intensity = intensity
        self.screenshake_step = intensity / duration
    
    def handle_screenshake(self):
        self.screenshake_timer = max(0, self.screenshake_timer - 1)
        if self.screenshake_timer > 0:
            self.screenshake_offset = pygame.Vector2(
                randf(-self.screenshake_intensity, self.screenshake_intensity, 0.1),
                randf(-self.screenshake_intensity, self.screenshake_intensity, 0.1),
            )
            self.screenshake_intensity -= self.screenshake_step
        else:
            self.screenshake_offset = pygame.Vector2(0, 0)
    
    def set_boundary(self, boundary: pygame.Rect):
        """Set a boundary for the camera to stay within."""
        self.boundary = boundary

    @property
    def rect(self):
        """Get the camera's current rectangle in the game world."""
        return pygame.Rect(
            self.pos.x - self.size.x // 2,
            self.pos.y - self.size.y // 2,
            self.size.x, 
            self.size.y,
        )

    def move_to(self, target_pos: pygame.Vector2, smoothing: float = 0.2, instant: bool = False):
        """Move the camera smoothly towards a target position."""
        if instant:
            self.pos = target_pos
        else:
            cos_smoothing = (1 - np.cos(smoothing * np.pi)) / 2
            self.pos = self.pos * (1 - cos_smoothing) + target_pos * cos_smoothing

        self.pos = self.clamp(self.pos, self.size, self.boundary)
        
    def clamp(self, pos: pygame.Vector2, size: Vec2, boundary: pygame.Rect) -> pygame.Vector2:
        clamped = pos
        if boundary:
            h_width = size.x // 2
            h_height = size.y // 2
            clamped = pygame.Vector2(
                max(boundary.left + h_width, min(int(pos.x), boundary.right - h_width)),
                max(boundary.top + h_height, min(int(pos.y), boundary.bottom - h_height))
            )
        return clamped
    