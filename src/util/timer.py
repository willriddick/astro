import pygame 

class Timer:
    def __init__(self, duration: int = 0):
        """Create a new timer with a duration in milliseconds."""
        self.duration = duration
        self.start_time = None
    
    def start(self, duration: int | None = None) -> None:
        if duration is not None:
            self.duration = duration
        self.start_time = pygame.time.get_ticks()
    
    def reset(self) -> None:
        self.start_time = None
    
    @property
    def time_left(self) -> float:
        if self.start_time is None:
            return 0
        return max(0, self.duration - (pygame.time.get_ticks() - self.start_time))
    
    @property
    def is_done(self) -> bool:
        return self.time_left == 0
    
    @property
    def is_active(self) -> bool:
        return self.time_left > 0
