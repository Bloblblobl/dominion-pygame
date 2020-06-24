import os
import pygame

from constants import zoom_factor


def load_image(image_path):
    try:
        image = pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f'Unable to load image: {image_path}')
        raise SystemExit(e)
    return image


def load_card_images(path, card_size):
    card_images = {}
    for filename in os.listdir(path):
        image_name = filename.split('.')[0]
        image_path = os.path.join(path, filename)
        small_image = pygame.transform.scale(load_image(image_path), card_size)
        zoom_image = pygame.transform.scale(load_image(image_path), list((d * zoom_factor for d in card_size)))
        card_images[image_name] = dict(small_image=small_image, zoom_image=zoom_image)

    return card_images
