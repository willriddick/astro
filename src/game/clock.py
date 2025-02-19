import pygame
import src.game.settings as settings

class Clock:
    """A global clock for our game."""
    _clock = pygame.time.Clock()
    _dt = 0

    @classmethod
    def update(cls):
        """
        Run every game tick.
        
        Updates delta time to `_clock.tick() / 1000` since `tick()` returns milliseconds.
        """
        cls._dt = cls._clock.tick(settings.get('max_fps')) / 1000

    @classmethod
    def dt(cls) -> float:
        """Returns the time in seconds since last frame."""
        return cls._dt
    
    @classmethod
    def fps(cls) -> int:
        """Returns the current frames per second as an int."""
        return int(cls._clock.get_fps())
    
    @classmethod
    def ticks(cls) -> int:
        """Returns times since pygame.init() was called in milliseconds."""
        return pygame.time.get_ticks()
