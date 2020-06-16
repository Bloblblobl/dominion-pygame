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
border_size = 4
card_size = 100, 160
speed = [0, 0]
background_color = 157, 206, 210

screen = pygame.display.set_mode(screen_size)

image_folder = 'images'
card_back_name = 'back'
card_images = util.load_card_images(image_folder, card_size)
card_names = [filename.split('.')[0] for filename in os.listdir('images') if not filename.startswith(card_back_name)]
cards = [Card(name, card_images[name], card_images[card_back_name], card_size) for name in card_names]
total_card_size = (cards[0].total_width, cards[0].total_height)

hand = CardView(cards, 5, card_size, draggable=False, spacing=10)
hand.x, hand.y = 0, height - hand.height
play_area = CardView(cards, 5, card_size, draggable=False, spacing=10)
play_area.x, play_area.y = 0, hand.y - hand.height
play_area.view_bg = None

draw_pile = CardStack(cards, card_size, False, (hand.x + hand.width + 10, hand.y))
discard_pile = CardStack(cards, card_size, True, (hand.x + hand.width + 20 + draw_pile.width, hand.y))
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
    screen.fill(background_color)
    hand.update(events, mouse_curr, mouse_delta)
    play_area.update(events, mouse_curr, mouse_delta)

    selected_card = hand.selected_card or play_area.selected_card

    hand.draw(screen)
    play_area.draw(screen)
    draw_pile.draw(screen)
    discard_pile.draw(screen)
    if selected_card is not None:
        screen.blit(selected_card.zoom, (screen_size[0] - card_size[0] * 2, 0))

    mouse_delta_text = font.render(f'Mouse ∆: {mouse_delta}', False, (255, 255, 255))
    screen.blit(mouse_delta_text, (5, 5))

    pygame.display.flip()

    mouse_prev = mouse_curr
