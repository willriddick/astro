from typing import NamedTuple
import pygame

class Vec2(NamedTuple):
    """
    An immutable 2D vector of ints (to use when pygame.Vector2 is overkill)
    
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
            direction (Direction): The direction to move in
        Returns:
            Vec2: A new Vec2 instance representing the updated position.
        """
    
        return Vec2(vec.x + direction.vector.x, vec.y + direction.vector.y)
    
    @staticmethod
    def to_vector2(vec: 'Vec2') -> pygame.Vector2:
        """
        Converts a Vec2 instance to a pygame.Vector2 instance.
        Args:
            vec (Vec2): The Vec2 instance to convert.
        Returns:
            pygame.Vector2: The equivalent pygame.Vector2 instance.
        """
        return pygame.Vector2(vec.x, vec.y)
