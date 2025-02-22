import pygame


class Clock:
    """A global class for managing the time clock."""
    
    def __init__(self):
        self._clock = pygame.time.Clock()
        self._dt = 0
    
    @property
    def dt(self) -> float:
        """Returns the time in seconds since the last frame."""
        return self._dt
    
    @property 
    def fps(self) -> int:
        """Returns the current frames per second as an int."""
        return int(self._clock.get_fps())
    
    @property
    def ticks(self) -> int:
        """Returns time since pygame.init() was called in milliseconds."""
        return pygame.time.get_ticks()

    def update(self):
        """Updates delta time to `_clock.tick() / 1000`."""
        self._dt = self._clock.tick() / 1000


CLOCK = Clock()
