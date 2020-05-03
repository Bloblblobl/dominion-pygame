import os
import pygame


def load_image(image_path):
    try:
        image = pygame.image.load(image_path)
    except pygame.error as e:
        print(f'Unable to load image: {image_path}')
        raise SystemExit(e)
    return image.convert()


def load_card_images(path, card_size):
    card_images = {}
    for filename in os.listdir(path):
        image_name = filename.split('.')[0]
        image_path = os.path.join(path, filename)
        small_image = pygame.transform.scale(load_image(image_path), card_size)
        zoom_image = pygame.transform.scale(load_image(image_path), list((d * 2 for d in card_size)))
        card_images[image_name] = dict(small_image=small_image, zoom_image=zoom_image)

    return card_images
