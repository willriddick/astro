from src.util import Vec2, draw_rect
from .components import Entity, Collider

class Gravity(Entity):
    def __init__(self, position, size: Vec2, multipier: float = 0.5):
        super().__init__(position, size)
        self.gravity_multiplier = multipier
        self.collider = Collider(size)
        self.collider.add_owner(self)
        self.collider.update(self.position)
    
    def render(self, display, offset):
        draw_rect(
            display=display,
            offset=offset,
            rect=self.collider.rect,
            fill_color=(80, 0, 150, 80),
        )