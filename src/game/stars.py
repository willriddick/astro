from random import choice, randint
import pygame
from src.util import Assets
from .components import Entity

class StarSpawner():
    def __init__(self):
        self.stars = []
        self.boundary: pygame.Rect | None = None
        self.buffer = 16
    
    def update(self):
        for star in self.stars:
            star.update()
        
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        for star in self.stars:
            star.render(display, offset)
    
    def spawn(self, count: int):
        for _ in range(count):
            self.stars.append(Star())
    
    def clear(self):
        self.starts.clear()

    def set_boundary(self, boundary: pygame.Rect):
        self.boundary = boundary.inflate(self.buffer, self.buffer)
    
class Star(Entity):
    def __init__(self):
        self.image = Assets.STARS[randint(0, len(Assets.STARS) - 1)]
        if choice([True, False]):
            self.image = pygame.transform.flip(self.image, True, False)

        self.position = pygame.Vector2(randint(0, 9999), randint(0, 9999))
        self.depth = randint(5, 60) / 200  # [0.025, .3]

        # alpha logic: closer stars (higher depth) should be brighter
        normalized_depth = (self.depth - 0.025) / (0.3 - 0.025)  
        max_alpha = 240  
        min_alpha = 40 
        alpha = min_alpha + (1 - normalized_depth) * (max_alpha - min_alpha)
        self.image.set_alpha(int(alpha))

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        # parallax effect: closer stars move more, distant stars move less
        render_pos = (self.position + offset) * self.depth
        width, height = self.image.get_size()
        display.blit(
            self.image, 
            (
                render_pos.x % (display.get_width() + width) - width, 
                render_pos.y % (display.get_height() + height) - height
            )
        )
