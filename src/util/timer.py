import pygame 

class Timer:
    def __init__(self, duration: float):
        self.duration = duration
        self.start_time = None
    
    def start(self) -> None:
        self.start_time = pygame.time.get_ticks()
    
    def reset(self) -> None:
        self.start_time = None
    
    def is_done(self) -> bool:
        if self.start_time is None:
            return True
        return (pygame.time.get_ticks() - self.start_time) >= self.duration
    
    def is_active(self) -> bool:
        return not self.is_done()
