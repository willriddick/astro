from math import sqrt, floor
from random import choice, choices, randint
import pygame
from src.util import Assets, randf
from src.game.components import Entity

class StarSpawner():
    def __init__(self, invert_depth: bool = False, buffer: int = 16):
        self.invert_depth = invert_depth
        self.buffer = buffer
        self.stars = []
    
    def update(self):
        for star in self.stars:
            star.update()
        
    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        for star in self.stars:
            star.render(display, offset)
    
    def spawn(self, count: int):
        for _ in range(count):
            self.stars.append(Star(self))
    
    def clear(self):
        self.stars.clear()
    
class Star(Entity):

    DEPTH = [0.05, 0.3]
    ALPHA = [20, 200]
    TINT_BASE = 220
    TINT_VARIATION = 35
    WEIGHTS: list[int] = []

    def __init__(self, spawner: StarSpawner):
        self.spawner = spawner

        # select a star image
        self.image = choices(Assets.STARS, weights=self.weights, k=1)[0].copy()

        # Adjust RGB values
        channel = randint(0, 2)
        r = Star.TINT_BASE + (Star.TINT_VARIATION if channel == 0 else randint(-Star.TINT_VARIATION, 0))
        g = Star.TINT_BASE + (Star.TINT_VARIATION if channel == 1 else randint(-Star.TINT_VARIATION, 0))
        b = Star.TINT_BASE + (Star.TINT_VARIATION if channel == 2 else randint(-Star.TINT_VARIATION, 0))

        # tint the star
        self.image.fill((r, g, b, 255), special_flags=pygame.BLEND_RGBA_MULT)

        # randomly flip the image
        self.image = pygame.transform.flip(self.image, choice([True, False]), choice([True, False]))

        # randomly position
        self.position = pygame.Vector2(randint(0, 9999), randint(0, 9999))

        # select a depth between 0.01
        # this number affects parallax speed and alpha
        self.depth = randf(*self.DEPTH, 0.01)
        self.inverted_depth = max(self.DEPTH) + min(self.DEPTH) - self.depth

        # alpha logic: closer stars (higher depth) should be brighter
        normalized_depth = (self.depth - Star.DEPTH[0]) / (Star.DEPTH[1] - Star.DEPTH[0])  
        alpha = Star.ALPHA[0] + (1 - normalized_depth) * (Star.ALPHA[1] - Star.ALPHA[0])
        self.image.set_alpha(int(alpha))

    @property
    def weights(self) -> list[int]:
        # if WEIGHTS has not been initialized
        if len(Star.WEIGHTS) == 0:
            length = len(Assets.STARS)
            # bias towards simpler starts
            for i in range(length):
                Star.WEIGHTS.append(floor(abs(i - length) * 3) + 5)
        
        # return weights
        return Star.WEIGHTS 

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        # parallax effect: closer stars move more, distant stars move less
        depth = self.inverted_depth if self.spawner.invert_depth else self.depth
        render_pos = (self.position + offset) * depth
        width, height = self.image.get_size()
        display.blit(
            self.image, 
            (
                render_pos.x % (display.get_width() + width) - width, 
                render_pos.y % (display.get_height() + height) - height
            )
        )
