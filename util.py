import os
import pygame

from constants import zoom_factor, card_back_name, card_size

from ui_elements.card import Card


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
        if filename.endswith('_gray.jpg'):
            continue
        image_name = filename.split('.')[0]
        image_path = os.path.join(path, filename)
        small_image = pygame.transform.scale(load_image(image_path), card_size)
        small_image_gray = pygame.transform.scale(load_image(image_path.replace('.jpg', '_gray.jpg')), card_size)
        zoom_image = pygame.transform.scale(load_image(image_path), list((d * zoom_factor for d in card_size)))
        card_images[image_name] = dict(small_image=small_image,
                                       small_image_gray=small_image_gray,
                                       zoom_image=zoom_image)

    return card_images


def create_card(card_name, card_images):
    image_name = card_name.lower()
    return Card(card_name, card_images[image_name], card_images[card_back_name], card_size)


action_cards = [c.strip() for c in """Bureaucrat
                                      Chancellor
                                      CouncilRoom
                                      Festival
                                      Library
                                      Militia
                                      Moat
                                      Spy
                                      Thief
                                      Village""".split()]


def is_action_card(card_name):
    return card_name in action_cards
