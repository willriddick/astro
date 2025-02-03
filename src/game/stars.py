from random import choice, choices, randint
import pygame
from src.util import Assets, randf
from .components import Entity

class StarSpawner():
    def __init__(self):
        self.stars = []
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
    
class Star(Entity):

    DEPTH = [0.01, 0.2]
    ALPHA = [40, 220]

    def __init__(self):
        weights = [len(Assets.STARS) - i for i in range(len(Assets.STARS))]  # gives higher weights to earlier images
        self.image = choices(Assets.STARS, weights=weights, k=1)[0]

        # randomly flip the image
        if choice([True, False]):
            self.image = pygame.transform.flip(self.image, True, False)

        # randomly position the image
        self.position = pygame.Vector2(randint(0, 9999), randint(0, 9999))

        # randomly select a depth between 0.01
        self.depth = randf(*self.DEPTH, 0.01)

        # alpha logic: closer stars (higher depth) should be brighter
        normalized_depth = (self.depth - Star.DEPTH[0]) / (Star.DEPTH[1] - Star.DEPTH[0])  
        alpha = Star.ALPHA[0] + (1 - normalized_depth) * (Star.ALPHA[1] - Star.ALPHA[0])
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
