from os.path import join
from os import listdir
import pygame


IMAGE_PATH = join('assets', 'images')
FONT_PATH = join('assets', 'fonts')

def load_image(path: str, convert_alpha: bool=True) -> pygame.Surface:
    try: 
        if convert_alpha:
            image = pygame.image.load(join(IMAGE_PATH, path)).convert_alpha()
        else:
            image = pygame.image.load(join(IMAGE_PATH, path)).convert()
        image.set_colorkey((0, 0, 0))
        return image
    except FileNotFoundError:
        print(f'Image {path} not found')
        raise

def load_images(path: str, convert_alpha: bool=False) -> list[pygame.Surface]:
    images = []
    for img_name in sorted(listdir(join(IMAGE_PATH, path))):
        images.append(load_image(join(path, img_name), convert_alpha))
    return images

def load_sprite_sheet(image: pygame.surface, size: tuple[int, int]) -> list[pygame.Surface]:
    cols = image.get_width() / size[0]
    rows = image.get_height() / size[1]

    assert cols.is_integer() and rows.is_integer(), (
        f'Sprite sheet size {size} does not evenly divide the image {image}'
    )
    cols, rows = int(cols), int(rows)

    images = []
    for y in range(rows):
        for x in range(cols):
            images.append(image.subsurface(x * size[0], y * size[1], size[0], size[1]).convert_alpha())
    return images

def load_font(path: str, size: int) -> pygame.font.Font:
    try:
        return pygame.font.Font(join(FONT_PATH, path), size)
    except FileNotFoundError:
        print(f'Font {path} not found')
        raise
