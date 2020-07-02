import os
import sys
import util
import pygame
import copy

from client.client import Client
from components.deck import Deck
from components.discard_pile import DiscardPile
from components.hand import Hand
from components.play_area import PlayArea
from components.shop import Shop
from components.side_panel import SidePanel
from constants import screen_size, card_size, background_color, font_name, card_back_name
from manager import Manager
from ui_elements.card import Card
from ui_player import UIPlayer

pygame.init()
pygame.font.init()
player = UIPlayer()
client = Client('test', player)
prev_state = None

screen = pygame.display.set_mode(screen_size)
screen_width, screen_height = screen_size
font = pygame.font.SysFont(font_name, 20)

image_folder = 'images'
card_images = util.load_card_images(image_folder, card_size)
card_names = [filename.split('.')[0] for filename in os.listdir('images') if not filename.startswith(card_back_name)]
cards = [Card(name, card_images[name], card_images[card_back_name], card_size) for name in card_names]
total_card_size = (cards[0].total_width, cards[0].total_height)

mouse_handlers = []


def main():
    """"""
    global prev_state

    mouse_prev = (0, 0)
    manager = Manager(None, None, None)

    hand = Hand([], manager.on_card_selected)
    deck = Deck(copy.copy(cards), top_face_up=False, pos=(hand.x + hand.width + 10, hand.y), on_click=manager.on_click)
    discard_pile = DiscardPile([], top_face_up=True, pos=(hand.x + hand.width + 20 + deck.width, hand.y))
    play_area = PlayArea([], manager.on_card_selected)
    shop = Shop([(card, 10) for card in copy.copy(cards[:16])], client)
    side_panel = SidePanel((shop.width + shop.spacing, 0), color=(0, 0, 0), game_client=client)
    mouse_handlers.append(side_panel.end_turn_button)
    mouse_handlers.append(side_panel.play_treasures_button)
    mouse_handlers.append(shop)

    manager.hand = hand
    manager.play_area = play_area
    manager.discard_pile = discard_pile

    while True:
        mouse_curr = pygame.mouse.get_pos()
        mouse_delta = (mouse_curr[0] - mouse_prev[0], mouse_curr[1] - mouse_prev[1])

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                for handler in mouse_handlers:
                    handler.handle_mouse_event(event.type, event.pos)

        screen.fill(background_color)
        selected_card = hand.selected_card or play_area.selected_card or shop.selected_card

        hand.update(events, mouse_curr, mouse_delta)
        play_area.update(events, mouse_curr, mouse_delta)
        deck.update(events, mouse_curr)
        shop.update()
        side_panel.update(events, mouse_curr, selected_card)

        client.pump()
        side_panel.players = client.players
        if player.state != prev_state:
            new_hand = player.state['hand']
            new_hand_cards = [util.create_card(card['name'], card_images) for card in new_hand]
            hand.cards = new_hand_cards

            new_shop = player.state['supply']
            new_card_counts = [(util.create_card(name, card_images), count) for name, count in new_shop.items()]
            shop.initialize_stacks(new_card_counts)

            side_panel.active_actions = player.state['actions']
            side_panel.active_buys = player.state['buys']
            side_panel.active_money = player.state['used_money']
            side_panel.message_log.messages.append(str(player.state))

            prev_state = player.state

        hand.draw(screen)
        play_area.draw(screen)
        deck.draw(screen)
        discard_pile.draw(screen)
        shop.draw(screen)
        side_panel.draw(screen)

        mouse_delta_text = font.render(f'Mouse ∆: {mouse_delta}', False, (255, 255, 255))
        screen.blit(mouse_delta_text,
                    (screen_width - mouse_delta_text.get_width(), screen_height - mouse_delta_text.get_height()))

        pygame.display.flip()

        mouse_prev = mouse_curr


if __name__ == '__main__':
    main()
