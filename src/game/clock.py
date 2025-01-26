import pygame

class Clock:
    """A global clock for our game."""
    _clock = pygame.time.Clock()
    _dt = 0

    @classmethod
    def update(cls):
        cls._dt = cls._clock.tick()

    @classmethod
    def dt(cls) -> float:
        """
        Returns the time in seconds since last frame.

        _clock.tick() returns the time in milliseconds since the last call to _clock.tick()
        so we divide _dt by 1000.
        """
        return cls._dt / 1000
    
    @classmethod
    def fps(cls):
        return cls._clock.get_fps()
