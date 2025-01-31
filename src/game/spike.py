import pygame
from src.util import Assets, Vec2
from src.game.components import Entity, Sprite, DamageComponent, Collider

class Spike(Entity):
    def __init__(self, level: 'Level', pos: pygame.Vector2):
        super().__init__(level, pos)
        self.level.entities.append(self)
        self.collider = Collider(
            level=self.level,
            size=Vec2(16, 2),
            offset=Vec2(0, 14)
        )
        self.collider.add_owner(self)
        self.damage_component = DamageComponent(self.collider, 1)
        self.damage_component.update(self.pos)
        
        self.sprite = Sprite(self.pos)
        self.sprite.add_animation(0, [Assets.SPIKE])
    
    def update(self):
        self.damage_component.update(self.pos)
