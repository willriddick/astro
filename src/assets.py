from os.path import join
import pygame
from src.util import load_image, load_sprite_sheet, load_palette, load_palettes, Vec2


ASSET_PATH = 'assets'

ICON = None
PALETTE = None
FONT = None
FONT_ILL = None
PLAYER_SHEET = None
PLAYER_PALETTES = None
STARS = None
ASTEROIDS = None
SPIKE = None
SOUNDS = None
TILESET = None

def load():
    """Load all assets into module-level variables."""
    global ICON, PALETTE, FONT, FONT_ILL, PLAYER_SHEET, PLAYER_PALETTES
    global STARS, ASTEROIDS, SPIKE, SOUNDS, TILESET

    ICON = load_image('icon.png', False)
    
    PALETTE = load_palette('endesga-64.png')
    
    FONT = pygame.font.Font(join(ASSET_PATH, join('fonts', 'DePixelKlein.ttf')), 9)

    PLAYER_SHEET = load_image(join('player', 'player.png'), False)
    PLAYER_PALETTES = load_palettes(join('player', 'palettes'))

    STARS = load_sprite_sheet(load_image('stars.png', True), (8, 8))
    ASTEROIDS = load_sprite_sheet(load_image('asteroids.png', True), (16, 16))
    SPIKE = load_sprite_sheet(load_image('spikes.png', True), (16, 16))

    _load_tileset()

def _load_tileset():
    """Initialize and store the tileset."""
    global TILESET
    from src.tilemap.tile_set import TileSet, TileType
    tileset = TileSet(Vec2(16, 16))

    test_tiles = load_sprite_sheet(load_image(join('tiles', 'test_tiles.png')), (16, 16))
    tileset.add(TileType('entrance', [test_tiles[0]]))
    tileset.add(TileType('exit', [test_tiles[1]]))

    tileset.add(TileType(
        name='stone',
        images=load_sprite_sheet(load_image(join('tiles', 'rock.png')), (16, 16)),
        collision=True,
        autotile=True,
    ))

    tileset.add(TileType(
        name='platform',
        images=[test_tiles[2]],
        collision=True,
        size=Vec2(16, 2),
    ))

    tileset.add(TileType(
        name='spike',
        images=[SPIKE[0]],
        size=Vec2(16, 2),
    ))

    TILESET = tileset
