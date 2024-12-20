import os
import pygame

BASE_IMG_PATH = 'assets/'

def load_image(path) -> pygame.Surface:
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path) -> list[pygame.Surface]:
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
    return images

def load_sprite_sheet(path: str, size: tuple[int, int]) -> list[pygame.Surface]:
    try:
        sheet = load_image(path)
    except FileNotFoundError:
        raise ValueError(f"Image file '{path}' not found")
    
    cols = sheet.get_width() / size[0]
    rows = sheet.get_height() / size[1]

    assert cols.is_integer() and rows.is_integer(), (
        f'Sprite sheet size {size} does not evenly divide the image at {path}'
    )
    cols, rows = int(cols), int(rows)

    images = []
    for y in range(rows):
        for x in range(cols):
            images.append(sheet.subsurface(x * size[0], y * size[1], size[0], size[1]).convert_alpha())
    return images
