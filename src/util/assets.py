import pygame

from .sound import Sounds
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
    SPIKE: list[pygame.Surface] = None
    STARS: list[pygame.Surface] = None
    EXIT: pygame.Surface = None
    SOUND_TEST: pygame.mixer.Sound = None

    SOUNDS: dict[str, pygame.mixer.Sound] = {}

    @staticmethod
    def load_assets():
        Assets.ICON = load_image('icon.png', False)

        Assets.FONT = pygame.font.Font(ASSET_PATH + 'fonts/DePixelKlein.ttf', 9)
        Assets.FONT_ILL = pygame.font.Font(ASSET_PATH + 'fonts/DePixelIllegible.ttf', 8)

        Assets.PLAYER_SHEET = load_image('player/player.png', False)
        Assets.PLAYER_PALETTES = load_palettes('player/palettes')

        Assets.STARS = load_sprite_sheet(load_image('stars.png', True), (8, 8))
        Assets.ASTEROIDS = load_sprite_sheet(load_image('asteroids.png', True), (16, 16))
        Assets.SPIKE = load_sprite_sheet(load_image('spikes.png', True), (16, 16))

        Assets.load_sounds()
        Assets.load_tileset()

    @staticmethod
    def load_sounds():
        Assets.SOUNDS = Sounds()
        Assets.SOUNDS.add('jump', volume=0.13, pitch_min=0.8, pitch_max=1.2, pitch_step=0.05)
        Assets.SOUNDS.add('land', 0.6, 0.9, 1.1, 0.05)
        Assets.SOUNDS.add('drop', 0.35, 0.9, 1.1, 0.05)
        Assets.SOUNDS.add('teleport', 0.2, 0.9, 1.1, 0.05)
        Assets.SOUNDS.add('hurt', 0.25, 0.9, 1.1, 0.05)
        Assets.SOUNDS.add('dead', 1.2, 0.9, 1.1, 0.05)
    
    @staticmethod
    def load_tileset():
        from src.tilemap.tile_set import TileSet, TileType
        Assets.TILESET = TileSet(Vec2(16, 16))

        test_tiles = load_sprite_sheet(load_image('tiles/test_tiles.png'), (16,16))
        Assets.TILESET.add(TileType('entrance', [test_tiles[0]],))
        Assets.TILESET.add(TileType('exit', [test_tiles[1]],))

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