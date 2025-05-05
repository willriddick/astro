import random
from os.path import join
import pygame
from src.util import (
    load_image, load_sprite_sheet, load_font, 
    load_palette, load_palettes, Vec2, swap_palette
)


LOGO = None
ICON = None
ICON_VARIANTS = None
PALETTE = None
FONT = None
PLAYER_SHEET = None
PLAYER_PALETTES = None
STARS = None
SPIKE = None
ROCKET = None
FUEL_CELL = None
TILESET = None


def load():
    """Load all assets into module-level variables."""
    global LOGO, ICON, ICON_VARIANTS, PALETTE, FONT, PLAYER_SHEET, PLAYER_PALETTES
    global STARS, SPIKE, TILESET, ROCKET, FUEL_CELL

    LOGO = load_image('logo.png', True)

    PALETTE = load_palette('endesga-64.png')
    FONT = load_font('DePixelKlein.ttf', 9)

    PLAYER_SHEET = load_image(join('player', 'player.png'), False)
    PLAYER_PALETTES = load_palettes(join('player', 'palettes'))

    ICON_VARIANTS = load_icon_variants()
    ICON = random.choice(ICON_VARIANTS)

    STARS = load_sprite_sheet(load_image('stars.png', True), (8, 8))
    SPIKE = load_sprite_sheet(load_image('spikes.png', True), (16, 16))
    ROCKET = load_image('rocket.png', True)
    FUEL_CELL = load_image('fuel_cell.png', True)

    _load_tileset()

def _load_tileset():
    """Initialize and store the tileset."""
    global TILESET
    from src.tilemap.tile_set import TileSet, TileType
    tileset = TileSet(Vec2(16, 16))

    extra = load_sprite_sheet(load_image(join('tiles', 'extra.png')), (16, 16))
    tileset.add(TileType('entrance', [extra[0]]))
    tileset.add(TileType('exit', [extra[1]]))
    tileset.add(TileType('collectable', [extra[2]]))

    tileset.add(TileType(
        name='stone',
        images=load_sprite_sheet(load_image(join('tiles', 'stone.png')), (16, 16)),
        collision=True,
        autotile=True,
    ))

    tileset.add(TileType(
        name='platform',
        images=[extra[3]],
        collision=True,
        size=Vec2(16, 2),
    ))

    tileset.add(TileType(
        name='spike',
        images=[SPIKE[0]],
        size=Vec2(16, 2),
    ))

    TILESET = tileset

def load_icon_variants() -> list[pygame.Surface]:
    """Load ICON variants with palette swaps for each player palette."""
    icon_variants = []
    icon = load_image('icon.png')

    for palette in PLAYER_PALETTES:
        swapped_icon = swap_palette(
            icon,
            PLAYER_PALETTES[0],
            palette
        )
        icon_variants.append(swapped_icon)

    return icon_variants
