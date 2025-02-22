import os
from typing import List
import pygame
from .load import load_image


IMAGE_PATH = os.path.join('assets', 'images')

Palette = List[pygame.color.Color]

def swap_color(image: pygame.Surface, old_color: pygame.color.Color, new_color: pygame.color.Color) -> pygame.Surface:
    image_copy = pygame.Surface(image.get_size())
    image_copy.fill(new_color)
    image.set_colorkey(old_color)
    image_copy.blit(image, (0, 0))
    image_copy.set_colorkey((0, 0, 0))
    return image_copy

def swap_palette(image: pygame.Surface, key_palette: Palette, new_palette: Palette) -> pygame.Surface:
    assert len(key_palette) == len(new_palette), f'Old ({len(key_palette)}) and new ({len(new_palette)}) palette must have the same size'
    for index, key_color in enumerate(key_palette):
        new_color = new_palette[index]
        image = swap_color(image, key_color, new_color)
    return image

def load_palette(path: str) -> Palette:
    image = load_image(path, False)
    size = image.get_size()
    assert size[1] == 1, f'Palette image must have a height of 1 pixel, got {size[0]}'
    return [image.get_at((x, 0)) for x in range(size[0])]

def load_palettes(path: str) -> list[Palette]:
    palettes = []
    for img_name in sorted(os.listdir(os.path.join(IMAGE_PATH, path))):
        palettes.append(load_palette(os.path.join(path, img_name)))
    return palettes
