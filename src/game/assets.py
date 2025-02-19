import pygame
from ..util.sound_manager import SoundManager
from ..util.load import load_image, load_sprite_sheet
from ..util.palette import load_palette, load_palettes
from ..util.vec2 import Vec2

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

ASSET_PATH = "assets/"

def load():
    """Load all assets into module-level variables."""
    global ICON, PALETTE, FONT, FONT_ILL, PLAYER_SHEET, PLAYER_PALETTES
    global STARS, ASTEROIDS, SPIKE, SOUNDS, TILESET

    ICON = load_image("icon.png", False)
    
    PALETTE = load_palette("endesga-64.png")
    
    FONT = pygame.font.Font(ASSET_PATH + "fonts/DePixelKlein.ttf", 9)
    FONT_ILL = pygame.font.Font(ASSET_PATH + "fonts/DePixelIllegible.ttf", 8)

    PLAYER_SHEET = load_image("player/player.png", False)
    PLAYER_PALETTES = load_palettes("player/palettes")

    STARS = load_sprite_sheet(load_image("stars.png", True), (8, 8))
    ASTEROIDS = load_sprite_sheet(load_image("asteroids.png", True), (16, 16))
    SPIKE = load_sprite_sheet(load_image("spikes.png", True), (16, 16))

    _load_sounds()
    _load_tileset()

def _load_sounds():
    """Initialize and store sounds using SoundManager."""
    global SOUNDS
    manager = SoundManager()
    manager.add(name="jump", vol=0.1, p_min=0.9, p_max=1.1, p_step=0.05)
    manager.add(name="wall_jump", path="jump", vol=0.1, p_min=0.7, p_max=1.8, p_step=0.05)
    manager.add("land", vol=0.35)
    manager.add("boost", vol=0.4)
    manager.add("cant_boost", vol=0.4)
    manager.add("slide", vol=0.35)
    manager.add("teleport", vol=0.2)
    manager.add("hurt", vol=0.25)
    manager.add("dead", vol=1.4)
    manager.add("blip_pitch", path="blip2", vol=0.5, p_min=0.8, p_max=1, p_step=0.025)
    manager.add("blip", path="blip2", vol=0.5, p_min=0.9, p_max=1.1, p_step=0.025)
    manager.add("select", path="select2", vol=0.4)
    
    manager.update_sounds()
    SOUNDS = manager

def _load_tileset():
    """Initialize and store the tileset."""
    global TILESET
    from src.tilemap.tile_set import TileSet, TileType
    tileset = TileSet(Vec2(16, 16))

    test_tiles = load_sprite_sheet(load_image("tiles/test_tiles.png"), (16, 16))
    tileset.add(TileType("entrance", [test_tiles[0]]))
    tileset.add(TileType("exit", [test_tiles[1]]))

    tileset.add(TileType(
        name="stone",
        images=load_sprite_sheet(load_image("tiles/rock.png"), (16, 16)),
        collision=True,
        autotile=True,
    ))

    tileset.add(TileType(
        name="platform",
        images=[test_tiles[2]],
        collision=True,
        size=Vec2(16, 2),
    ))

    tileset.add(TileType(
        name="spike",
        images=[SPIKE[0]],
        size=Vec2(16, 2),
    ))

    TILESET = tileset
