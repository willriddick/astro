from src.util import Assets, Vec2
from .components import Sprite, Entity, Collider

class Exit(Entity):
    def __init__(self, level, pos):
        super().__init__(level, pos)

        self.collider = Collider(
            level=self.level, 
            size=Vec2(16, 16), 
            offset=Vec2(0, 0)
        )
        self.collider.add_owner(self)
        self.collider.update(self.pos)
