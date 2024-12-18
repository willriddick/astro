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
