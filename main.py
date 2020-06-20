import os
import sys
import util
import pygame
import copy

from components.deck import Deck
from components.discard_pile import DiscardPile
from components.hand import Hand
from components.play_area import PlayArea
from components.shop import Shop
from constants import card_size, background_color, screen_size
from manager import Manager
from ui_elements.card import Card


pygame.init()
pygame.font.init()
screen = pygame.display.set_mode(screen_size)
screen_width, screen_height = screen_size
font = pygame.font.SysFont('arial', 20)

image_folder = 'images'
card_back_name = 'back'
card_images = util.load_card_images(image_folder, card_size)
card_names = [filename.split('.')[0] for filename in os.listdir('images') if not filename.startswith(card_back_name)]
cards = [Card(name, card_images[name], card_images[card_back_name], card_size) for name in card_names]
total_card_size = (cards[0].total_width, cards[0].total_height)


def main():
    """"""
    mouse_prev = (0, 0)
    manager = Manager(None, None, None)

    hand = Hand([], manager.on_card_selected)
    deck = Deck(copy.copy(cards), top_face_up=False, pos=(hand.x + hand.width + 10, hand.y), on_click=manager.on_click)
    discard_pile = DiscardPile([], top_face_up=True, pos=(hand.x + hand.width + 20 + deck.width, hand.y))
    play_area = PlayArea([], manager.on_card_selected)
    shop = Shop(copy.copy(cards[:16]))

    manager.hand = hand
    manager.play_area = play_area
    manager.discard_pile = discard_pile

    while True:
        mouse_curr = pygame.mouse.get_pos()
        mouse_delta = (mouse_curr[0] - mouse_prev[0], mouse_curr[1] - mouse_prev[1])

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: sys.exit()

        screen.fill(background_color)
        selected_card = hand.selected_card or play_area.selected_card

        hand.update(events, mouse_curr, mouse_delta)
        play_area.update(events, mouse_curr, mouse_delta)
        deck.update(events, mouse_curr)

        hand.draw(screen)
        play_area.draw(screen)
        deck.draw(screen)
        discard_pile.draw(screen)
        shop.draw(screen)

        if selected_card is not None:
            screen.blit(selected_card.zoom, (screen_size[0] - card_size[0] * 2, 0))

        mouse_delta_text = font.render(f'Mouse ∆: {mouse_delta}', False, (255, 255, 255))
        screen.blit(mouse_delta_text,
                    (screen_width - mouse_delta_text.get_width(), screen_height - mouse_delta_text.get_height()))

        pygame.display.flip()

        mouse_prev = mouse_curr

if __name__ == '__main__':
    main()
