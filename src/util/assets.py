import pygame
from .load import load_image, load_sprite_sheet

class Assets:
    FONT = None
    TILESET = None

    @staticmethod
    def load_assets():
        Assets.FONT = pygame.font.Font('assets/fonts/DePixelIllegible.ttf', 8)

        from src.tilemap.tile_set import TileSet 
        Assets.TILESET = TileSet(16)
        Assets.TILESET.add('stone', load_sprite_sheet(load_image('tileset/template.png'), (16,16)), True)
        Assets.TILESET.add('door', [load_sprite_sheet(load_image('items.png'), (16,16))[0]], False)
