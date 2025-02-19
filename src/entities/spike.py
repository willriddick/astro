import pygame
from src.util import Vec2
from src.components import Entity, Sprite, DamageComponent, Collider
import src.assets as assets

class Spike(Entity):
    def __init__(self, position: pygame.Vector2, size: Vec2):
        super().__init__(position, size)
        self.collider = None
        self.damage_component = None
        self.sprite = Sprite(self.position)
        self.sprite.add_animation(0, assets.SPIKE.copy())
        self.sprite.set_animation(0)

    def render(self, display, offset):
        self.sprite.render(display, offset)

class HSpike(Spike):
    def __init__(self, position: pygame.Vector2, width: int, above: bool = False):
        super().__init__(position, Vec2(16 * width, 16))
        self.width = width

        collider_size = Vec2(16 * width, 1)
        collider_offset = Vec2(0, 0) if above else Vec2(0, 15)
        self.collider = Collider(collider_size, collider_offset)
        self.collider.add_owner(self)

        self.damage_component = DamageComponent(self.collider, 1)
        self.damage_component.update(self.position)

        self.sprite.flip_y = above
        self.sprite.set_frame(0)

    def render(self, display, offset):
        """Render each segment of the horizontal spike."""
        for i in range(self.width):
            self.sprite.render(display, offset + pygame.Vector2(i * 16, 0))

class VSpike(Spike):
    def __init__(self, position: pygame.Vector2, height: int, right: bool = False):
        super().__init__(position, Vec2(16, 16 * height))
        self.height = height

        collider_size = Vec2(1, 16 * height)
        collider_offset = Vec2(14, 0) if right else Vec2(1, 0)
        self.collider = Collider(collider_size, collider_offset)
        self.collider.add_owner(self)

        self.damage_component = DamageComponent(self.collider, 1)
        self.damage_component.update(self.position)

        self.sprite.flip_x = right
        self.sprite.set_frame(1)

    def render(self, display, offset):
        """Render each segment of the vertical spike."""
        for i in range(self.height):
            self.sprite.render(display, offset + pygame.Vector2(0, i * 16))

class CSpike(Spike):
    def __init__(self, position: pygame.Vector2, above: bool, right: bool):
        super().__init__(position, Vec2(16, 16))
        if above:
            offset1 = Vec2(0, 0)
            self.sprite.flip_y = True
        else:
            offset1 = Vec2(0, 15)
        
        if right:
            offset2 = Vec2(14, 0)
            self.sprite.flip_x = True
        else:
            offset2 = Vec2(1, 0)
        
        self.collider1 = Collider(Vec2(16, 1), offset1)
        self.collider1.add_owner(self)
        self.collider2 = Collider(Vec2(1, 16), offset2)
        self.collider2.add_owner(self)
        self.damage_component = DamageComponent([self.collider1, self.collider2], 1)
        self.damage_component.update(self.position)

        self.sprite.set_frame(2)
