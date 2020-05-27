import os
import sys
import util
import pygame
from card import Card
from cardstack import CardStack
from cardview import CardView

pygame.init()
pygame.font.init()

screen_size = width, height = 1080, 700
real_card_size = 100, 160
border_size = 4
card_size = [i + border_size for i in real_card_size]
speed = [0, 0]
black = 0, 0, 0

screen = pygame.display.set_mode(screen_size)

image_folder = 'images'
card_images = util.load_card_images(image_folder, real_card_size)
card_names = [filename.split('.')[0] for filename in os.listdir('images')]
cards = [Card(name, card_images[name], card_size) for name in card_names]

cardview = CardView(cards, 5, card_size, draggable=False, spacing=10)
cardview.x, cardview.y = 0, height - cardview.height
cardstack = CardStack(cards, card_size, False, (cardview.x + cardview.width + 10, cardview.y))
font = pygame.font.SysFont('arial', 30)
mouse_prev = (0, 0)

while 1:
    mouse_curr = pygame.mouse.get_pos()
    mouse_delta = (mouse_curr[0] - mouse_prev[0], mouse_curr[1] - mouse_prev[1])

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: sys.exit()

    # cardstack.update(events)
    # cardstack.draw(screen)
    screen.fill(black)
    cardview.update(events, mouse_delta)
    cardview.draw(screen)
    cardstack.draw(screen)

    mouse_delta_text = font.render(f'Mouse ∆: {mouse_delta}', False, (255, 255, 255))
    screen.blit(mouse_delta_text, (5, 5))

    pygame.display.flip()

    mouse_prev = mouse_curr
