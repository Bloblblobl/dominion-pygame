import os
import pygame

image_folder = 'images'


def load_image(name):
    image_path = os.path.join(image_folder, name)
    try:
        image = pygame.image.load(image_path)
    except pygame.error as e:
        print(f'Unable to load image: {image_path}')
        raise SystemExit(e)
    return image.convert()


def balance_val(minval, maxval, val):
    val = max(val, minval)
    val = min(val, maxval)
    return val
