from typing import NamedTuple

class Vec2(NamedTuple):
    """An immutable 2D vector (to use when pygame.Vector2 is overkill)"""
    x: int
    y: int

    @staticmethod
    def move(vec: 'Vec2', direction: 'Direction') -> 'Vec2':
        """Returns a new Vec2 object moved in the direction passed."""
        return Vec2(vec.x + direction.vector.x, vec.y + direction.vector.y)
