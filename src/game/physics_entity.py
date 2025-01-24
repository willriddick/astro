import pygame
from src.tilemap import TileMap
from src.util import approach, Direction, Vec2
from .entity import Entity

class PhysicsEntity(Entity):
    def __init__(self, level: 'Level', pos: pygame.Vector2, size: Vec2):
        super().__init__(level, pos)
        self.size = size
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
   
    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.rect.center)
    
    @property
    def rect(self) -> pygame.FRect:
        return pygame.FRect(self.pos.x, self.pos.y, self.size.x, self.size.y)
    
    def apply_force(self, force: float, direction: Direction | pygame.Vector2):
        self.velocity = force * (direction.vector if isinstance(direction, Direction) else direction)
    
    def accelerate_x(self, dir_: int, max_speed: float, acc: tuple[float, float]):
        self.velocity.x = self.accelerate_decelerate(self.velocity.x, max_speed, dir_, acc, self.velocity_multiplier.x)
    
    def accelerate_y(self, dir_: int, max_speed: float, acc: tuple[float, float]):
        self.velocity.y = self.accelerate_decelerate(self.velocity.y, max_speed, dir_, acc, self.velocity_multiplier.y)
    
    def apply_gravity(self, gravity: float, max_speed: float):
        self.velocity.y = min(
            max_speed * self.gravity_multiplier,
            self.velocity.y + gravity * self.gravity_multiplier
        )

    @staticmethod
    def accelerate_decelerate(value: float, target: float, dir_: int, acc: tuple[float, float], multiplier: float) -> float:
        if dir_ == 0:
            return approach(
                value=value,
                target=0,
                step=acc[1] * multiplier
            )
        else:
            return approach(
                value=value,
                target=dir_ * target * multiplier,
                step=acc[0] * multiplier
            )

    def handle_collision(self, tilemap: TileMap):
        if not self.collision_enabled:
            self.pos += self.velocity
            return

        # Update tile position
        tile_pos = Vec2(int(self.pos.x) // tilemap.tile_size.x, int(self.pos.y) // tilemap.tile_size.y)
        self.tiles_around = tilemap.get_tiles_around(tile_pos)

        # Handle platform collision
        for platform in filter(lambda _tile: _tile.tile_type.name == 'platform', self.tiles_around):
            # If player is below platform, disable collision
            if platform.rect.top < self.rect.bottom:
                platform.collision = False
            else:
                if self.on_ground and self.drop_down:
                    platform.collision = False
                else:
                    platform.collision = True

        # Filter out collision tiles
        collisions_around = list(filter(lambda _tile: _tile.collision, self.tiles_around))

        # Update y position
        self.pos.y += self.velocity.y
        entity_rect = self.rect
        for tile in collisions_around:
            rect = tile.rect
            if entity_rect.colliderect(rect):
                if self.velocity.y > 0:
                    entity_rect.bottom = rect.top
                    self.pos.y = entity_rect.y
                    self.velocity.y = 0
                if self.velocity.y < 0:
                    entity_rect.top = rect.bottom
                    self.pos.y = entity_rect.y
                    self.velocity.y = 0

        # Update x position
        self.pos.x += self.velocity.x
        entity_rect = self.rect
        for tile in collisions_around:
            rect = tile.rect
            if entity_rect.colliderect(rect):
                if self.velocity.x > 0:
                    entity_rect.right = rect.left
                    self.pos.x = entity_rect.x
                    self.velocity.x = 0
                if self.velocity.x < 0:
                    entity_rect.left = rect.right
                    self.pos.x = entity_rect.x
                    self.velocity.x = 0
        
        # Update collisions
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
