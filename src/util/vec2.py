from typing import NamedTuple, Union
import pygame


class Vec2(NamedTuple):
    """
    An immutable 2D vector of ints (to use when pygame.Vector2 is overkill).
    
    Example:
       `size = Vec2(10, 20)`
    """
    x: int
    y: int

    @staticmethod
    def translate(vec: 'Vec2', direction: 'Direction') -> 'Vec2':
        """
        Returns a new Vec2 instance translated in the given direction.
        Args:
            vec (Vec2): The original position.
            direction (Direction): The direction to move in.
        Returns:
            Vec2: A new Vec2 instance representing the updated position.
        """
        return Vec2(vec.x + direction.vector.x, vec.y + direction.vector.y)

    def to_vector2(self) -> pygame.Vector2:
        """ Converts this Vec2 to a pygame.Vector2 instance. """
        return pygame.Vector2(self.x, self.y)

    @staticmethod
    def from_vector2(vec: pygame.Vector2) -> 'Vec2':
        """ Converts a pygame.Vector2 instance to a Vec2 (rounded to ints). """
        return Vec2(int(vec.x), int(vec.y))

    def __add__(self, other: Union['Vec2', pygame.Vector2]) -> 'Vec2':
        """ Supports addition with both Vec2 and pygame.Vector2. """
        if isinstance(other, pygame.Vector2):
            return Vec2(int(self.x + other.x), int(self.y + other.y))
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Union['Vec2', pygame.Vector2]) -> 'Vec2':
        """ Supports subtraction with both Vec2 and pygame.Vector2. """
        if isinstance(other, pygame.Vector2):
            return Vec2(int(self.x - other.x), int(self.y - other.y))
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: int) -> 'Vec2':
        """ Supports scalar multiplication. """
        return Vec2(self.x * scalar, self.y * scalar)

    def __repr__(self) -> str:
        """ Returns a readable representation of the Vec2 instance. """
        return f"Vec2({self.x}, {self.y})"
