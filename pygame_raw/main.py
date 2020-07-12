import os
import sys
from pygame_raw import util
import pygame
import copy
from pathology.path import Path

from client.client import Client
from pygame_raw.components.deck import Deck
from pygame_raw.components.discard_pile import DiscardPile
from pygame_raw.components.hand import Hand
from pygame_raw.components.play_area import PlayArea
from pygame_raw.components.shop import Shop
from pygame_raw.components.side_panel import SidePanel
from pygame_raw.constants import screen_size, card_size, background_color, font_name, card_back_name, WHITE
from pygame_raw.manager import Manager
from pygame_raw.ui_elements.button import Button
from pygame_raw.ui_elements.card import Card
from ui_player import UIPlayer

pygame.init()
pygame.font.init()
player = UIPlayer()
client = Client('test', player) # , '10.0.0.72')
prev_state = None

screen = pygame.display.set_mode(screen_size)
screen_width, screen_height = screen_size
font = pygame.font.SysFont(font_name, 20)

image_folder = str((Path.script_dir() / '../images').resolve())
card_images = util.load_card_images(image_folder, card_size)

card_names = [filename.split('.')[0] for filename in os.listdir(image_folder) if not filename.startswith(card_back_name)]
card_names = [n for n in card_names if not n.endswith('_gray')]
cards = [Card(name, card_images[name], card_images[card_back_name], card_size) for name in card_names]
total_card_size = (cards[0].total_width, cards[0].total_height)

mouse_handlers = []


def start_game_handler(source):
    source.show = False
    client.start_game()
    del mouse_handlers[-1]


def main():
    """"""
    global prev_state

    mouse_prev = (0, 0)
    manager = Manager(client, None, None, None)

    hand = Hand([], manager.on_card_selected)
    deck = Deck(copy.copy(cards), top_face_up=False, pos=(hand.x + hand.width + 10, hand.y), on_click=manager.on_click)
    discard_pile = DiscardPile([], top_face_up=True, pos=(hand.x + hand.width + 20 + deck.width, hand.y))
    play_area = PlayArea([], manager.on_card_selected)
    shop = Shop([(card, 10) for card in copy.copy(cards[:16])], client)
    side_panel = SidePanel((shop.width + shop.spacing, 0), color=(0, 0, 0), game_client=client)
    side_button = side_panel.play_treasures_button
    start_button_pos = (side_button.x, side_button.y)
    start_game_button = Button(start_button_pos,
                               side_button.width,
                               side_button.height,
                               text='Start Game',
                               on_click=start_game_handler)
    start_game_button.show = True

    mouse_handlers.append(side_panel.end_turn_button)
    mouse_handlers.append(side_panel.play_treasures_button)
    mouse_handlers.append(shop)
    mouse_handlers.append(start_game_button)

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
        if start_game_button.show:
            start_game_button.update()

        client.pump()
        side_panel.players = client.players
        if player.state != prev_state:
            new_actions = player.state['actions']
            new_buys = player.state['buys']
            new_money = player.state['used_money']

            new_hand = player.state['hand']
            new_hand_cards = [util.create_card(card['name'], card_images) for card in new_hand]
            hand.cards = new_hand_cards
            hand.view_bg = None

            new_play_area = player.state['play_area']
            print(new_play_area)
            new_play_area_cards = [util.create_card(card['name'], card_images) for card in new_play_area]
            play_area.cards = new_play_area_cards

            new_deck = player.state['draw_deck']
            new_deck_cards = [
                util.create_card(card_name, card_images) for card_name, count in new_deck.items() for _ in range(count)
            ]
            deck.cards = new_deck_cards

            new_discard = player.state['discard_pile']
            new_discard_cards = [util.create_card(card['name'], card_images) for card in new_discard]
            discard_pile.cards = new_discard_cards

            new_shop = player.state['supply']
            new_card_counts = [(util.create_card(name, card_images), count) for name, count in new_shop.items()]
            shop.initialize_stacks(new_card_counts)
            shop.background_color = None

            side_panel.active_actions = new_actions
            side_panel.active_buys = new_buys
            side_panel.active_money = new_money

            if not side_panel.message_log.messages:
                side_panel.message_log.messages.extend(client.card_names)

            prev_state = player.state

        if player.message_queue:
            side_panel.message_log.messages.extend(player.message_queue)
            player.message_queue = []

        #no_action_cards = not any(util.is_action_card(c.name) for c in hand.cards)
        #disabled = player.state is not None and (player.state['actions'] == 0 or no_action_cards)
        disabled = player.state is not None and player.state['actions'] == 0
        hand.draw(screen, disabled=disabled)
        play_area.draw(screen)
        deck.draw(screen)
        discard_pile.draw(screen)
        disabled = player.state is not None and player.state['buys'] == 0
        shop.draw(screen, disabled=disabled)
        side_panel.draw(screen)
        if start_game_button.show:
            start_game_button.draw(screen)

        mouse_delta_text = font.render(f'Mouse ∆: {mouse_delta}', False, WHITE)
        screen.blit(mouse_delta_text,
                    (screen_width - mouse_delta_text.get_width(), screen_height - mouse_delta_text.get_height()))

        pygame.display.flip()

        mouse_prev = mouse_curr


if __name__ == '__main__':
    main()
