import pygame
from src.util import Vec2
from ..level import Level 
from .sprite import Sprite

class Entity:
    """
    An entity is in object that can be placed within the game world.

    Attributes:
    - position (pygame.Vector2): The position of the entity.
    - size (Vec2): The size of the entity.
    - offset (pygame.Vector2): The offset of the entity.

    Properties:
    - rect (pygame.FRect): The rect of the entity at `position` + `offset` with `size`.
    - tile_position (Vec2): The tile position of the entity.
    - center (pygame.Vector2): The center of the entity's rect.
    - bottom_center (pygame.Vector2): The bottom center of the entity's rect.
    - sprite (Sprite | None): The sprite of the entity.

    Methods:
    - update(): Update the entity.
    - render(display: pygame.Surface, offset: pygame.Vector2): Render the entity's sprite.
    """
    def __init__(self, position: pygame.Vector2, size: Vec2, offset = pygame.Vector2(0, 0)):
        self.position = position
        self.size = size
        self.offset = offset
        self.sprite: Sprite | None = None
    
    def update(self) -> None:
        pass

    def render(self, display: pygame.Surface, offset: pygame.Vector2) -> None:
        if self.sprite:
            self.sprite.render(display, offset)

    @property
    def rect(self) -> pygame.FRect:
        return pygame.FRect(
            self.position.x + self.offset.x,
            self.position.y + self.offset.y,
            self.size.x,
            self.size.y
        )
    
    @property
    def tile_position(self) -> Vec2:
        tile_size = Level.current.tilemap.tile_size
        return Vec2(
            int(self.position.x) // tile_size.x,
            int(self.position.y) // tile_size.y
        )

    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)
    
    @property
    def bottom_center(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.centerx, self.rect.bottom)
    