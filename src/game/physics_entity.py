import pygame
from src.util import approach

class PhysicsEntity(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], rect_size: tuple[int, int]):
        super().__init__()
        self.pos = pygame.Vector2(pos)
        self.rect_size = rect_size

        self.velocity = pygame.Vector2(0, 0)
    
    def accelerate_x(self, dir_: int, max_speed: float, acc: tuple[float, float]):
        self.velocity.x = self.accelerate_decelerate(self.velocity.x, max_speed, dir_, acc)
    
    def accelerate_y(self, dir_: int, max_speed: float, acc: tuple[float, float]):
        self.velocity.y = self.accelerate_decelerate(self.velocity.y, max_speed, dir_, acc)

    def accelerate_decelerate(self, value: float, target: float, dir_: int, acc: tuple[float, float]) -> float:
        if dir_ == 0:
            return approach(
                value=value,
                target=0,
                step=acc[1] * self.movement_multiplier
            )
        else:
            return approach(
                value=value,
                target=dir_ * target * self.movement_multiplier,
                step=acc[0] * self.movement_multiplier
            )
   