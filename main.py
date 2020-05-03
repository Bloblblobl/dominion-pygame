import os
import sys
import util
import pygame
from card import Card
from cardstack import CardStack

pygame.init()

screen_size = width, height = 1000, 600
card_size = 154, 239
real_card_size = 150, 235
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(screen_size)

image_folder = 'images'
card_images = util.load_card_images(image_folder, real_card_size)
card_names = [filename.split('.')[0] for filename in os.listdir('images')]
cards = [Card(name, card_images[name], card_size) for name in card_names]
cardstack = CardStack(cards, screen_size, card_size)

while 1:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    cardstack.update(events)
    cardstack.draw(screen)
    pygame.display.flip()
