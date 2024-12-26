from enum import Enum
from src.util import load_sprite_sheet
from ..sprite import Sprite

class Animation(Enum):
    IDLE = 0
    RUN = 1
    AIR_UP = 2
    AIR_DOWN = 3
    FRONT = 4
    BACK = 5

def add_animations(sprite: Sprite):
    sprite.add_animation(Animation.IDLE, load_sprite_sheet('player/idle.png', (32, 32)), 0)
    sprite.add_animation(Animation.RUN, load_sprite_sheet('player/run.png', (32, 32)), 10)
    sprite.add_animation(Animation.AIR_UP, load_sprite_sheet('player/air_up.png', (32, 32)), 0)
    sprite.add_animation(Animation.AIR_DOWN, load_sprite_sheet('player/air_down.png', (32, 32)), 0)
    sprite.add_animation(Animation.FRONT, load_sprite_sheet('player/front.png', (32, 32)), 0)
    sprite.add_animation(Animation.BACK, load_sprite_sheet('player/back.png', (32, 32)), 0)
