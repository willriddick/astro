import pygame

from .load import load_image, load_images, load_sprite_sheet 
from .palette import Palette, load_palettes
from .vec2 import Vec2

ASSET_PATH = 'assets/'

class Assets:
    ICON: pygame.Surface = None
    FONT: pygame.Font = None
    TILESET = None
    PLAYER_SHEET: pygame.Surface = None
    PLAYER_PALETTES: list[Palette] = None
    ASTEROIDS: list[pygame.Surface] = None
    SPIKE: pygame.Surface = None
    GRAVITY: pygame.Surface = None
    STARS: pygame.Surface = None
    EXIT: pygame.Surface = None
    SOUND_TEST: pygame.mixer.Sound = None

    @staticmethod
    def load_assets():
        test_tiles = load_sprite_sheet(load_image('tiles/test_tiles.png'), (16,16))

        Assets.ICON = load_image('icon.png', False)

        Assets.SOUND_TEST = pygame.mixer.Sound(ASSET_PATH + 'sounds/s1.wav')

        Assets.FONT = pygame.font.Font(ASSET_PATH + 'fonts/DePixelKlein.ttf', 9)
        Assets.FONT_ILL = pygame.font.Font(ASSET_PATH + 'fonts/DePixelIllegible.ttf', 8)

        Assets.PLAYER_SHEET = load_image('player/player.png', False)
        Assets.PLAYER_PALETTES = load_palettes('player/palettes')

        Assets.STARS = load_sprite_sheet(load_image('stars.png', True), (8, 8))
        Assets.ASTEROIDS = load_images('asteroids', True)

        Assets.SPIKE = load_sprite_sheet(load_image('spikes.png', True), (16, 16))
        Assets.GRAVITY = test_tiles[4]

        from src.tilemap.tile_set import TileSet, TileType
        Assets.TILESET = TileSet(Vec2(16, 16))

        Assets.TILESET.add(TileType('entrance', [test_tiles[0]],))
        Assets.TILESET.add(TileType('exit', [test_tiles[1]],))
        Assets.TILESET.add(TileType('gravity', [Assets.GRAVITY]))

        Assets.TILESET.add(TileType(
            name='stone', 
            images=load_sprite_sheet(load_image('tiles/rock.png'), (16,16)), 
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
            images=[Assets.SPIKE[0]],
            size=Vec2(16, 2),
        ))
    