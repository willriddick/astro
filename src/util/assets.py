import pygame
from .load import load_image, load_images, load_sprite_sheet 
from .palette import Palette, load_palettes
from .types import Vec2

ASSET_PATH = 'assets/'

class Assets:
    FONT: pygame.Font = None
    TILESET = None
    PLAYER_SHEET: pygame.Surface = None
    PLAYER_PALETTES: list[Palette] = None
    ASTEROIDS: list[pygame.Surface] = None

    @staticmethod
    def load_assets():
        Assets.FONT = pygame.font.Font(ASSET_PATH + 'fonts/DePixelIllegible.ttf', 8)

        from src.tilemap.tile_set import TileSet 
        Assets.TILESET = TileSet(Vec2(16, 16))
        Assets.TILESET.add('stone', load_sprite_sheet(load_image('tileset/template.png'), (16,16)), True)
        Assets.TILESET.add('door', [load_sprite_sheet(load_image('items.png'), (16,16))[0]], False)
        Assets.TILESET.add('test', [load_sprite_sheet(load_image('items.png'), (16,16))[1]], False)

        Assets.PLAYER_SHEET = load_image('player/player.png', False)
        Assets.PLAYER_PALETTES = load_palettes('player/palettes')

        Assets.ASTEROIDS = load_images('asteroids', True)
