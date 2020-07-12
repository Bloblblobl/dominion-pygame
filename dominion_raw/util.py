import os
from glob import glob

import pygame

from .constants import zoom_factor, card_back_name, card_size

from .ui_elements.card import Card


def load_image(image_path):
    try:
        image = pygame.image.load(image_path).convert_alpha()
    except pygame.error as e:
        print(f'Unable to load image: {image_path}')
        raise SystemExit(e)
    return image


def load_card_images(images_dir, card_size):
    card_images = {}
    for filename in glob(os.path.join(images_dir, '*.png')):
        if filename.endswith('_gray.png') or filename.endswith('_pic.png'):
            continue
        image_name = os.path.basename(filename).split('.')[0]
        image = load_image(filename)
        small_image = pygame.transform.scale(image, card_size)
        small_image_gray = pygame.transform.scale(load_image(filename.replace('.png', '_gray.png')), card_size)
        zoom_image = pygame.transform.scale(image, list((d * zoom_factor for d in card_size)))
        card_images[image_name] = dict(small_image=small_image,
                                       small_image_gray=small_image_gray,
                                       zoom_image=zoom_image)

    return card_images


def create_card(card_name, card_images):
    image_name = card_name.lower()
    return Card(card_name, card_images[image_name], card_images[card_back_name], card_size)


action_cards = [c.strip() for c in """Bureaucrat                                      
                                      CouncilRoom
                                      Festival
                                      Library
                                      Market
                                      Militia
                                      Moat
                                      Smithy
                                      Village
                                      Witch""".split()]


def is_action_card(card_name):
    return card_name in action_cards
