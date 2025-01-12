import pygame
from typing import List
from .surface import load_image, load_sprite_sheet, load_palette

Palette = List[pygame.color.Color]

class Assets:
    FONT: pygame.Font = None
    TILESET = None
    PLAYER_SHEET: pygame.Surface = None
    PLAYER_PALETTES: list[Palette] = None

    @staticmethod
    def load_assets():
        Assets.FONT = pygame.font.Font('assets/fonts/DePixelIllegible.ttf', 8)

        from src.tilemap.tile_set import TileSet 
        Assets.TILESET = TileSet(16)
        Assets.TILESET.add('stone', load_sprite_sheet(load_image('tileset/template.png'), (16,16)), True)
        Assets.TILESET.add('door', [load_sprite_sheet(load_image('items.png'), (16,16))[0]], False)

        Assets.PLAYER_SHEET = load_image('player/player.png', False)
        Assets.PLAYER_PALETTES = [
            load_palette('player/palette_key.png'),
            load_palette('player/palette1.png'),
            load_palette('player/palette2.png'),
            load_palette('player/palette3.png'),
            load_palette('player/palette4.png'),
        ]
