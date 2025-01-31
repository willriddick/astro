import pygame
from src.tilemap import Tile
from src.util import approach, Direction, Vec2
from ..level import Level
from .entity import Entity
from ..clock import Clock

class PhysicsEntity(Entity):
    def __init__(self, position: pygame.Vector2, size: Vec2, offset = pygame.Vector2(0, 0)):
        super().__init__(position, size, offset)
        self.velocity = pygame.Vector2(0, 0)
        self.velocity_multiplier = pygame.Vector2(1, 1)
        self.gravity_multiplier = 1

        # Collision
        self.tiles_around = []
        self.falling = False
        self.on_ground = False
        self.drop_down = False
        self.collision_enabled = True
        self.collisions = { 
            Direction.UP: False,
            Direction.DOWN: False,
            Direction.RIGHT: False, 
            Direction.LEFT: False
        }
   
    def apply_force(self, force: float, direction: Direction | pygame.Vector2):
        self.velocity = force * (direction.vector if isinstance(direction, Direction) else direction)
    
    def accelerate_x(self, dir_: int, speed: float, acc: tuple[float, float]):
        self.velocity.x = self._acc_dec(self.velocity.x, speed, dir_, acc, self.velocity_multiplier.x)
    
    def accelerate_y(self, dir_: int, speed: float, acc: tuple[float, float]):
        self.velocity.y = self._acc_dec(self.velocity.y, speed, dir_, acc, self.velocity_multiplier.y)
    
    def apply_gravity(self, gravity: float, fall_speed: float):
        self.velocity.y = min(
            fall_speed * self.gravity_multiplier,
            self.velocity.y + (gravity * self.gravity_multiplier * Clock.dt())
        )

    @staticmethod
    def _acc_dec(value: float, target: float, dir_: int, acc: tuple[float, float], multiplier: float) -> float:
        if dir_ != 0:
            target = dir_ * target * multiplier
            step = acc[0] * multiplier * Clock.dt()
        else:
            target = 0
            step = acc[1] * multiplier * Clock.dt()

        return approach(value, target, step)

    def handle_collision(self):
        if not self.collision_enabled:
            self.position += (self.velocity * Clock.dt())
            return

        # Update tile position
        tilemap = Level.current.tilemap
        self.tiles_around = tilemap.get_tiles_around(self.tile_position)

        # Handle platform collision
        self._handle_platform_collision() 

        # Filter out collision tiles
        collisions_around = list(filter(lambda _tile: _tile.collision, self.tiles_around))

        # Update y position
        self.position.y += (self.velocity.y * Clock.dt())
        entity_rect = self.rect
        for tile in collisions_around:
            rect = tile.rect
            if entity_rect.colliderect(rect):
                if self.velocity.y > 0:
                    entity_rect.bottom = rect.top
                    self.position.y = entity_rect.y
                    self.velocity.y = 0
                if self.velocity.y < 0:
                    entity_rect.top = rect.bottom
                    self.position.y = entity_rect.y
                    self.velocity.y *= 0.85

        # Update x position
        self.position.x += (self.velocity.x * Clock.dt())
        entity_rect = self.rect
        for tile in collisions_around:
            rect = tile.rect
            if entity_rect.colliderect(rect):
                if self.velocity.x > 0:
                    entity_rect.right = rect.left
                    self.position.x = entity_rect.x
                    self.velocity.x = 0
                if self.velocity.x < 0:
                    entity_rect.left = rect.right
                    self.position.x = entity_rect.x
                    self.velocity.x = 0
        
        self._update_collision_flags(entity_rect, collisions_around)
    
    def _handle_platform_collision(self): 
        for platform in filter(lambda _tile: _tile.tile_type.name == 'platform', self.tiles_around):
            # If player is below platform, disable collision
            if platform.rect.top < self.rect.bottom:
                platform.collision = False
            else:
                if self.on_ground and self.drop_down:
                    platform.collision = False
                else:
                    platform.collision = True

    def _update_collision_flags(self, entity_rect: pygame.Rect, collisions_around: list[Tile]):
        points = {
            Direction.DOWN:  [(entity_rect.left + 1,  entity_rect.bottom + 1),
                              (entity_rect.right - 1, entity_rect.bottom + 1)],
            Direction.UP:    [(entity_rect.left + 1,  entity_rect.top - 1),
                              (entity_rect.right - 1, entity_rect.top - 1)],
            Direction.LEFT:  [(entity_rect.left - 1,  entity_rect.top + 1),
                              (entity_rect.left - 1,  entity_rect.bottom - 1)],
            Direction.RIGHT: [(entity_rect.right + 1, entity_rect.top + 1),
                              (entity_rect.right + 1, entity_rect.bottom - 1)],
        }

        for direction, points in points.items():
            self.collisions[direction] = False
            for tile in collisions_around:
                tile_rect = tile.rect
                if any(tile_rect.collidepoint(point) for point in points):
                    self.collisions[direction] = True
                    break # No need to check further tiles for this direction
        
        # Update helper variables
        self.on_ground = self.collisions[Direction.DOWN]
        self.falling = (self.velocity.y > 0 and not self.collisions[Direction.DOWN])
