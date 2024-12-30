import pygame
from src.tilemap import Tilemap
from src.util import approach, Direction

class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], rect_size: tuple[int, int]):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.rect_size = rect_size

        # Velocity
        self.velocity = pygame.Vector2(0, 0)
        self.velocity_multiplier = pygame.Vector2(1, 1)

        # Gravity
        self.gravity_multiplier = 1
        self.gravity = 0.14
        self.fall_speed = 3

        # Collision
        self.tiles_around = []
        self.falling = False
        self.on_ground = False
        self.collisions = { 
            Direction.UP: False,
            Direction.DOWN: False,
            Direction.RIGHT: False, 
            Direction.LEFT: False
        }

        # Sprite
        self.sprite = None
    
    def render(self, display, offset=(0, 0)):
        if self.sprite:
            self.sprite.render(display, offset)
    
    def set_animation(self, animation: int):
        if self.sprite:
            self.sprite.set_animation(animation)
   
    def accelerate_x(self, dir_: int, max_speed: float, acc: tuple[float, float]):
        self.velocity.x = self.accelerate_decelerate(self.velocity.x, max_speed, dir_, acc, self.velocity_multiplier.x)
    
    def accelerate_y(self, dir_: int, max_speed: float, acc: tuple[float, float]):
        self.velocity.y = self.accelerate_decelerate(self.velocity.y, max_speed, dir_, acc, self.velocity_multiplier.y)
    
    def apply_gravity(self, gravity: float, max_speed: float, ):
        self.velocity.y = min(
            max_speed * self.gravity_multiplier,
            self.velocity.y + gravity * self.gravity_multiplier
        )

    def accelerate_decelerate(self, value: float, target: float, dir_: int, acc: tuple[float, float], multiplier: float) -> float:
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
    
    def get_rect(self):
        return pygame.FRect(self.pos.x, self.pos.y, self.rect_size[0], self.rect_size[1])
    
    def handle_collision(self, tilemap: Tilemap):
        # Update tile position
        tile_pos = (self.pos.x // tilemap.tile_size, self.pos.y // tilemap.tile_size)
        self.tiles_around = tilemap.get_tiles_around(tile_pos, ['stone'])

        # Update y position
        self.pos.y += self.velocity.y
        entity_rect = self.get_rect()
        for tile in self.tiles_around:
            rect = tile.get_rect()
            if entity_rect.colliderect(rect):
                if self.velocity.y > 0:
                    entity_rect.bottom = rect.top
                if self.velocity.y < 0:
                    entity_rect.top = rect.bottom
                self.pos.y = entity_rect.y
                self.velocity.y = 0

        # Update x position
        self.pos.x += self.velocity.x
        entity_rect = self.get_rect()
        for tile in self.tiles_around:
            rect = tile.get_rect()
            if entity_rect.colliderect(rect):
                if self.velocity.x > 0:
                    entity_rect.right = rect.left
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
            for tile in self.tiles_around:
                tile_rect = tile.get_rect()
                if any(tile_rect.collidepoint(point) for point in points):
                    self.collisions[direction] = True
                    break # No need to check further tiles for this direction
                else:
                    self.collisions[direction] = False
        
        # Update helper variables
        self.on_ground = self.collisions[Direction.DOWN]
        self.falling = (self.velocity.y > 0 and not self.collisions[Direction.DOWN])


   