import random
import pygame
from src.util import Vec2
from src.clock import CLOCK
from src.components import PhysicsEntity, Entity, Sprite
import src.graphics as graphics


class AsteroidSpawner(Entity):
    def __init__(self):
        super().__init__(pygame.Vector2(0, 0), Vec2(0, 0))
        self.asteroids = []
        self.boundary: pygame.Rect | None = None
        self.buffer = 16
    
    def spawn(self, count: int):
        for _ in range(count):
            new_asteroid = Asteroid(self)
            self.reset_asteroid(new_asteroid)
            self.asteroids.append(new_asteroid)
    
    def reset_asteroid(self, asteroid: 'Asteroid'):
        # Get random speed 
        x_vel = random.choice([-50, -25, 25, 50])
        y_vel = random.choice([-50, -25, 25, 50])
        
        # Pick spawn position along boundary
        if random.randint(0, 1):
            x = random.choice([self.boundary.left, self.boundary.right])
            y = random.randint(self.boundary.top, self.boundary.bottom)

            y_vel *= random.choice([-1, 1])
            if x == self.boundary.right:
                x_vel *= -1
        else:
            x = random.randint(self.boundary.left, self.boundary.right)
            y = random.choice([self.boundary.top, self.boundary.bottom])

            x *= random.choice([-1, 1])
            if y == self.boundary.bottom:
                y_vel *= -1

        # Set asteroid properties
        asteroid.position = pygame.Vector2(x, y)
        asteroid.velocity = pygame.Vector2(x_vel, y_vel)
        asteroid.sprite.set_frame(random.randint(0, len(graphics.ASTEROIDS) - 1))
    
    def clear(self):
        self.asteroids.clear()

    def set_boundary(self, boundary: pygame.Rect):
        self.boundary = boundary.inflate(self.buffer, self.buffer)
        
    def update(self):
        for asteroid in self.asteroids:
            asteroid.update()

    def render(self, display: pygame.Surface, offset: pygame.Vector2):
        for asteroid in self.asteroids:
            asteroid.render(display, offset)


class Asteroid(PhysicsEntity):
    def __init__(self, spawner: AsteroidSpawner):
        super().__init__(pygame.Vector2(0, 0), Vec2(16, 16))
        self.spawner = spawner
        self.sprite = Sprite(self.position, Vec2(0, 0))
        self.sprite.add_animation(0, graphics.ASTEROIDS, 0)
    
    def __str__(self):
        return f'asteroid: position={self.position}, vel={self.velocity}, frame={self.sprite.frame}'
    
    def update(self):
        self.position += (self.velocity * CLOCK.dt)
        self.sprite.update(self.position)
        
        if not self.spawner.boundary.collidepoint(self.center):
            self.spawner.reset_asteroid(self)
