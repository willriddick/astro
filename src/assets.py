import pygame
from src.util import SoundManager, Sound, load_image, load_sprite_sheet, load_palette, load_palettes, Vec2

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
    SOUNDS = SoundManager()
    SOUNDS.load_all([
        Sound("jump", default_volume=0.2, pitch=[0.9, 1.1, 0.05]),
        Sound("wall_jump", path="jump", default_volume=0.2, pitch=[0.7, 1.8, 0.05]),
        Sound("land", default_volume=0.7),
        Sound("boost", default_volume=0.8),
        Sound("cant_boost", default_volume=0.8),
        Sound("slide", default_volume=0.7),
        Sound("teleport", default_volume=0.4),
        Sound("hurt", default_volume=0.5),
        Sound("dead", default_volume=2.8),
        Sound("blip_pitch",  path="blip2", default_volume=1, pitch=[0.7, 1.2, 0.03]),
        Sound("blip", path="blip2", default_volume=1, pitch=[0.9, 1.1, 0.025]),
        Sound("select", default_volume=0.8, path="select2"),
        Sound("music/track1", default_volume=0.8),
    ])

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
