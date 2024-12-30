import os
import pygame

BASE_IMG_PATH = 'assets/'

def load_image(path: str, convert_alpha: bool=True) -> pygame.Surface:
    try: 
        if convert_alpha:
            image = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
        else:
            image = pygame.image.load(BASE_IMG_PATH + path).convert()
        image.set_colorkey((0, 0, 0))
        return image
    except FileNotFoundError:
        print(f'Image {path} not found')
        raise

def load_images(path: str, convert_alpha: bool=False) -> list[pygame.Surface]:
    images = []
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, convert_alpha))
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

def swap_color(image: pygame.Surface, old_color: pygame.color.Color, new_color: pygame.color.Color) -> pygame.Surface:
    image_copy = pygame.Surface(image.get_size())
    image_copy.fill(new_color)
    image.set_colorkey(old_color)
    image_copy.blit(image, (0, 0))
    image_copy.set_colorkey((0, 0, 0))
    return image_copy

def swap_palette(image: pygame.Surface, old_palette: list[pygame.color.Color], new_palette: list[pygame.color.Color]) -> pygame.Surface:
    assert len(old_palette) == len(new_palette), f'Old ({len(old_palette)}) and new ({len(new_palette)}) palette must have the same size'
    for index, old_color in enumerate(old_palette):
        new_color = new_palette[index]
        image = swap_color(image, old_color, new_color)
    return image

def load_palette(path: str) -> list[pygame.color.Color]:
    image = load_image(path, False)
    size = image.get_size()
    assert size[1] == 1, f'Palette image must have a heigth of 1 pixel, got {size[0]}'
    return [image.get_at((x, 0)) for x in range(size[0])]
