import pygame
from src.graphics import PLAYER_SHEET, PLAYER_PALETTES
from src.util import Vec2, swap_palette, load_sprite_sheet
from src.components import Sprite
from .player import Player 
from .enums import Animations

def load_sprite(palette_index: int) -> tuple[Sprite, pygame.Color]:
    palette_index = palette_index % len(PLAYER_PALETTES)
    palette = PLAYER_PALETTES[palette_index]

    fuel_ui_color = palette[Player.FUEL_UI_COLOR_INDEX]

    sheet = swap_palette(
        PLAYER_SHEET,
        PLAYER_PALETTES[0],
        palette,
    )
    image_list = load_sprite_sheet(sheet, (16, 18))
    
    sprite = Sprite(pygame.Vector2(0, 0), image_offset=Vec2(4, 5))
    sprite.add_animation(Animations.IDLE_A, image_list, 0, range_=(0,1))
    sprite.add_animation(Animations.IDLE_B, image_list, 5, range_=(0,4))
    sprite.add_animation(Animations.RUN, image_list, 12, range_=(4,10))
    sprite.add_animation(Animations.AIR_UP, image_list, 0, range_=(10,11))
    sprite.add_animation(Animations.AIR_DOWN, image_list, 0, range_=(11,12))
    sprite.add_animation(Animations.FRONT, image_list, 0, range_=(12,13))
    sprite.add_animation(Animations.BACK, image_list, 0, range_=(13,14))
    sprite.add_animation(Animations.WALL_SLIDE, image_list, 0, range_=(14,15))
    sprite.add_animation(Animations.SLIDE, image_list, 0, range_=(15,16))
    sprite.add_animation(Animations.BOOST_UP, image_list, 0, range_=(16,17))
    sprite.add_animation(Animations.BOOST_DOWN, image_list, 0, range_=(16,17))

    return sprite, fuel_ui_color