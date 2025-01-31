import pygame
from src.util import Assets, Vec2
from src.game.components import Entity, Sprite, DamageComponent, Collider

class Spike(Entity):
    def __init__(self, position: pygame.Vector2):
        super().__init__(position, Vec2(16, 16))
        self.collider = Collider(
            size=Vec2(14, 1),
            offset=Vec2(1, 15)
        )
        self.collider.add_owner(self)
        self.damage_component = DamageComponent(self.collider, 1)
        self.damage_component.update(self.position)
        
        self.sprite = Sprite(self.position)
        self.sprite.add_animation(0, [Assets.SPIKE])
    
    def update(self):
        self.damage_component.update(self.postion)
