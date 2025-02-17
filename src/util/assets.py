import pygame

from .sound_manager import SoundManager
from .load import load_image, load_sprite_sheet 
from .palette import Palette, load_palette, load_palettes
from .vec2 import Vec2

ASSET_PATH = 'assets/'

class Assets:
    ICON: pygame.Surface = None
    FONT: pygame.Font = None
    PALETTE: Palette = None
    PLAYER_SHEET: pygame.Surface = None
    PLAYER_PALETTES: list[Palette] = None
    TILESET = None
    ASTEROIDS: list[pygame.Surface] = None
    SPIKE: list[pygame.Surface] = None
    STARS: list[pygame.Surface] = None
    EXIT: pygame.Surface = None

    MUSIC: pygame.mixer.Sound = None

    @staticmethod
    def load():
        Assets.ICON = load_image('icon.png', False)

        Assets.PALETTE = load_palette('endesga-64.png')

        Assets.FONT = pygame.font.Font(ASSET_PATH + 'fonts/DePixelKlein.ttf', 9)
        Assets.FONT_ILL = pygame.font.Font(ASSET_PATH + 'fonts/DePixelIllegible.ttf', 8)

        Assets.PLAYER_SHEET = load_image('player/player.png', False)
        Assets.PLAYER_PALETTES = load_palettes('player/palettes')

        Assets.STARS = load_sprite_sheet(load_image('stars.png', True), (8, 8))
        Assets.ASTEROIDS = load_sprite_sheet(load_image('asteroids.png', True), (16, 16))
        Assets.SPIKE = load_sprite_sheet(load_image('spikes.png', True), (16, 16))

        Assets._load_sounds()
        Assets._load_tileset()

    @staticmethod
    def _load_sounds():
        manager = SoundManager()
        manager.add(name='jump', vol=0.1, p_min=0.9, p_max=1.1, p_step=0.05)
        manager.add(name='wall_jump', path="jump", vol=0.1, p_min=0.7, p_max=1.8, p_step=0.05)
        manager.add('land', vol=0.35)
        manager.add('boost', vol=0.4)
        manager.add('cant_boost', vol=0.4)
        manager.add('slide', vol=0.35)
        manager.add('teleport', vol=0.2)
        manager.add('hurt', vol=0.25)
        manager.add('dead', vol=1.4)
        manager.add('blip_pitch', path='blip', vol=0.15, p_min=0.4, p_max=0.7, p_step=0.025)
        manager.add('blip', vol=0.15, p_min=0.5, p_max=0.6, p_step=0.025)
        manager.add('select', vol=0.1)
        #manager.add('track1', path='music/track1', category=1, vol=0.2)
        #manager.add('track2', path='music/track2', category=1, vol=0.1)
        #manager.add('track2r', path='music/track2r', category=1, vol=0.1)
        manager.update_sounds()
        Assets.SOUNDS = manager
    
    @staticmethod
    def _load_tileset():
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