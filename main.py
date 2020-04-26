import os
import sys
import pygame
from card import Card
from cardstack import CardStack

pygame.init()

size = width, height = 1000, 600
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

card_names = [filename for filename in os.listdir('images')]
cards = [Card(name) for name in card_names]
# copper = Card('copper.jpg')
# silver = Card('silver.jpg')
# gold = Card('gold.jpg')
cardstack = CardStack(cards)
cardstack.scale(300, 480)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    pressed_keys = pygame.key.get_pressed()
    cardstack.update(pressed_keys)
    cardstack.draw(screen)
    pygame.display.flip()
