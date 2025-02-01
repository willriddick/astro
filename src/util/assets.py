import pygame

from .load import load_image, load_images, load_sprite_sheet 
from .palette import Palette, load_palettes
from .vec2 import Vec2

ASSET_PATH = 'assets/'

class Assets:
    FONT: pygame.Font = None
    TILESET = None
    PLAYER_SHEET: pygame.Surface = None
    PLAYER_PALETTES: list[Palette] = None
    ASTEROIDS: list[pygame.Surface] = None
    SPIKE: pygame.Surface = None
    GRAVITY: pygame.Surface = None
    EXIT: pygame.Surface = None

    @staticmethod
    def load_assets():
        test_tiles = load_sprite_sheet(load_image('test_tiles.png'), (16,16))

        Assets.FONT = pygame.font.Font(ASSET_PATH + 'fonts/DePixelKlein.ttf', 9)
        Assets.FONT_ILL = pygame.font.Font(ASSET_PATH + 'fonts/DePixelIllegible.ttf', 8)

        Assets.PLAYER_SHEET = load_image('player/player.png', False)
        Assets.PLAYER_PALETTES = load_palettes('player/palettes')

        Assets.STARS = load_sprite_sheet(load_image('stars.png', True), (8, 8))
        Assets.ASTEROIDS = load_images('asteroids', True)

        Assets.SPIKE = test_tiles[3]
        Assets.GRAVITY = test_tiles[4]

        from src.tilemap.tile_set import TileSet, TileType
        Assets.TILESET = TileSet(Vec2(16, 16))

        Assets.TILESET.add(TileType('entrance', [test_tiles[0]],))
        Assets.TILESET.add(TileType('exit', [test_tiles[1]],))
        Assets.TILESET.add(TileType('gravity', [Assets.GRAVITY]))

        Assets.TILESET.add(TileType(
            name='stone', 
            images=load_sprite_sheet(load_image('tileset/template.png'), (16,16)), 
            collision=True,
            autotile=True,
        ))

        Assets.TILESET.add(TileType(
            name='platform', 
            images=[test_tiles[2]],
            collision=True,
            size=Vec2(16, 2),
        ))

        Assets.TILESET.add(TileType(
            name='spike', 
            images=[Assets.SPIKE],
            size=Vec2(16, 2),
        ))
    