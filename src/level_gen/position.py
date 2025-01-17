from typing import NamedTuple
from math import sqrt
from src.util import Direction

class Position(NamedTuple):
    """
    A class representing a 2D position with x and y coordinates.
    Attributes:
        x (int): The x-coordinate of the position.
        y (int): The y-coordinate of the position.
    """
    x: int
    y: int

    def __str__(self) -> str:
        return f'({self.x},{self.y})' 

    def __add__(self, other: 'Position') -> 'Position':
        """Add two Position objects together."""
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Position') -> 'Position':
        """Subtract one Position from another."""
        return Position(self.x - other.x, self.y - other.y)

    def __eq__(self, other: object) -> bool:
        """
        Check for equality between two Position instances.
        Args:
            other (object): The other object to compare.
        Returns:
            bool: True if both positions are equal, False otherwise.
        """
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def distance_to(self, other: 'Position') -> float:
        """
        Calculate the Euclidean distance between two positions.
        Args:
            other (Position): The other position to measure distance to.
        Returns:
            float: The Euclidean distance between the two positions.
        """
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def move(self, direction: Direction) -> 'Position':
        """
        Return a new position after movement in the provided direction.
        Args:
            direction (Direction): The direction in which to move.
        Returns:
            Position: The new Position after movement.
        """
        movement_vector = Position(*direction.vector)  
        return self + movement_vector  
    