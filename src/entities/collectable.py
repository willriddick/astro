from ..components import Entity, Collider, Sprite
import src.graphics as graphics

class Collectable(Entity):
    def __init__(self, position, size):
        super().__init__(position, size)
        self.sprite = Sprite(position)
        self.sprite.add_animation(0, graphics.ASTEROIDS, 0, (0, 1))
        
        self.collider = Collider(size)
        self.collider.add_owner(self)
        self.collider.update(position)

        self.collected = False
    
    def collect(self, entity: Entity):
        print(f'{entity} collected {self}')
        self.collected = True
        self.collider.enabled = False
        self.sprite.alpha = 50
    