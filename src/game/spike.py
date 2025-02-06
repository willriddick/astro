import pygame
from src.util import Assets, Vec2
from src.game.components import Entity, Sprite, DamageComponent, Collider

class Spike(Entity):
    def __init__(
            self, 
            position: pygame.Vector2,
            width: int = 1,
            height: int = 1,
            above: bool = False,
            below: bool = False
        ):
        super().__init__(position, Vec2(16, 16))

        self.width = width 
        self.height = height
        self.above = above
        self.below = below

        if height == 1:
            collider_size = Vec2(16 * width, 1)
            if self.above:
                collider_offset = Vec2(0, 0)
            else:
                collider_offset = Vec2(0, 15)
        elif width == 1:
            collider_size = Vec2(1, 16 * height)
            collider_offset = Vec2(15, 0)
        
        self.collider = Collider(collider_size, collider_offset)

        self.collider.add_owner(self)
        self.damage_component = DamageComponent(self.collider, 1)
        self.damage_component.update(self.position)
        
        self.sprite = Sprite(self.position)
        self.sprite.flip_y = above 
        self.sprite.add_animation(0, Assets.SPIKE)
    
    def render(self, display, offset):
        for i in range(self.width):
            self.sprite.render(display, offset + pygame.Vector2(i * self.size.x, 0))
    