import pygame

from .sound import change_pitch
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
        Assets.SOUNDS['jump'] = change_pitch(pygame.mixer.Sound(ASSET_PATH + 'sounds/jump.wav'), 0.8)
        Assets.SOUNDS['jump'].set_volume(0.07)

        Assets.SOUNDS['land'] = pygame.mixer.Sound(ASSET_PATH + 'sounds/land.wav')
        Assets.SOUNDS['land'].set_volume(0.6)

        Assets.SOUNDS['drop'] = pygame.mixer.Sound(ASSET_PATH + 'sounds/drop.wav')
        Assets.SOUNDS['drop'].set_volume(0.35)

        Assets.SOUNDS['teleport'] = pygame.mixer.Sound(ASSET_PATH + 'sounds/teleport.wav')
        Assets.SOUNDS['teleport'].set_volume(0.2)

        Assets.SOUNDS['hurt'] = pygame.mixer.Sound(ASSET_PATH + 'sounds/hurt.wav')
        Assets.SOUNDS['hurt'].set_volume(0.25)

        Assets.SOUNDS['dead'] = pygame.mixer.Sound(ASSET_PATH + 'sounds/explosion.wav')
        Assets.SOUNDS['dead'].set_volume(1.2)
    
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