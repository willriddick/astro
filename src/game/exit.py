from src.util import Assets, Vec2
from .components import Sprite, Entity, Collider

class Exit(Entity):
    def __init__(self, pos):
        super().__init__(pos)

        self.collider = Collider(
            size=Vec2(16, 16), 
            offset=Vec2(0, 0)
        )
        self.collider.add_owner(self)
        self.collider.update(self.pos)
