import pygame
import numpy as np
from src.game.level import Level
from src.util import Vec2
from .entity import Entity

class Camera:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.display = pygame.Surface((width, height))

        # In-game positions
        self.position = pygame.Vector2(0, 0)
        self.target_position = pygame.Vector2(0, 0)
        self.offset = pygame.Vector2(0, 0)
        self.boundary: pygame.Rect | None = None

        self.level: Level | None = None

        self.fill_color = (24, 20, 37)
    
    def update(self):
        """Update the camera and render the display surface."""
        # Clear display surface
        self.display.fill(self.fill_color)

        # Calculate the offset from the in-game position
        self.offset = pygame.Vector2(
            self.position.x - self.width // 2,
            self.position.y - self.height // 2
        )

        # Render the tilemap  
        self.render_tilemap(self.level.tilemap)

        # Render all entities relative to the offset
        for entity in self.level.entities:
            entity.render(self.display, -self.offset)
        
        # Render all colliders
        for collider in self.level.colliders:
            collider.render(self.display, -self.offset)

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
        
    def get_rect(self):
        """Get the camera's current rectangle in the game world."""
        return pygame.Rect(
            self.position.x - self.width // 2,
            self.position.y - self.height // 2,
            self.width, self.height
        )

    def move_to(self, target: pygame.Vector2, smoothing: float = 0.2, instant: bool = False):
        """Move the camera smoothly towards a target position."""
        self.target_position = target

        if instant:
            self.position = self.target_position
        else:
            cos_smoothing = (1 - np.cos(smoothing * np.pi)) / 2
            self.position = self.position * (1 - cos_smoothing) + self.target_position * cos_smoothing

        # Clamp the camera's position to the boundary if defined
        if self.boundary:
            clamped_x = max(
                self.boundary.left + self.width // 2,
                min(int(self.position.x), self.boundary.right - (self.width // 2))
            )
            clamped_y = max(
                self.boundary.top + self.height // 2,
                min(int(self.position.y), self.boundary.bottom - (self.height // 2))
            )
            self.position = pygame.Vector2(clamped_x, clamped_y)
    
    def set_boundary(self, boundary: pygame.Rect):
        """Set a boundary for the camera to stay within."""
        self.boundary = boundary

    def draw_debug(self):
        camera_marker = pygame.Rect(self.width // 2 - 2, self.height // 2 - 2, 4, 4)
        target_marker = pygame.Rect(
            self.width // 2 + (self.target_position.x - self.position.x) - 2,
            self.height // 2 + (self.target_position.y - self.position.y) - 2,
            4, 4
        )
        offset_marker = pygame.Rect(self.offset.x, self.offset.y, 4, 4)
        pygame.draw.rect(self.display, (255, 255, 255), camera_marker, 1)
        pygame.draw.rect(self.display, (255, 0, 0), target_marker, 1)
        pygame.draw.rect(self.display, (0, 0, 255), offset_marker, 1)
