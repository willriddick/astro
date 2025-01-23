import pygame
from src.util import Assets, Vec2
from .entity import Entity
from .damage import DamageComponent
from .collider import Collider
from .sprite import Sprite

class Spike(Entity):
    def __init__(self, level: 'Level', pos: pygame.Vector2):
        super().__init__(level, pos, Vec2(16, 2))
        self.level.entities.append(self)
        print(self.pos)
        self.damage_component = DamageComponent(1)
        self.damage_component.collider = Collider(self.level, self.damage_component, Vec2(16, 2), Vec2(0, 14))
        self.damage_component.update(self.pos)
        
        self.sprite = Sprite(self.pos)
        self.sprite.add_animation(0, [Assets.SPIKE])
        self.sprite.set_animation(0)
    