from src.util import Vec2
from src.game.components import Entity, Collider

class Exit(Entity):
    def __init__(self, position):
        super().__init__(position, Vec2(16, 16))

        self.collider = Collider(
            size=Vec2(16, 16), 
            offset=Vec2(0, 0)
        )
        self.collider.add_owner(self)
        self.collider.update(self.position)
