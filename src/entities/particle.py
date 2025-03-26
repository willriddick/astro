import pygame
from src.components import Entity
from src.util import Vec2


class Particle(Entity):
    def __init__(self, size: Vec2):
        super().__init__((0, 0), size)

    def update(self):
        pass

    def render(self, display, offset):
        pass

    def spawn(self):
        pass

    def despawn(self):
        pass
