import os
import sys

import pygame
import pygame_gui

from constants import root_dir

sys.path.append(root_dir)

from dominion_gui import game_client, util

from dominion_gui.event_handler import EventHandler, MouseButton
from dominion_gui.constants import screen_size, preloaded_fonts, min_screen_width, min_screen_height, \
    DISPLAY_FLAGS
import dominion_gui.event_manager as em
from dominion_gui.responder import Responder
from dominion_gui.ui_manager import get_manager
from dominion_gui.ui_factory import UI
from dominion_gui.ui_player import UIPlayer

# Replace for each player until we have a name selection in the UI
player_name = 'Gigi'


class DominionApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dominion')
        self.surface = pygame.display.set_mode(screen_size, flags=DISPLAY_FLAGS)
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.state = None

        manager = get_manager(screen_size)
        manager.preload_fonts(preloaded_fonts)

        self.ui = UI()
        self.game_client = game_client.get_instance(player_name)
        self.join()
        self.player = UIPlayer(self.game_client)
        self.event_manager = em.get_event_manager(self.ui.window)
        handler = EventHandler()
        handler.on_ui_button_press = lambda ui_element: self.start()
        handler.on_custom_event = self.on_custom_game_event
        self.event_manager.subscribe(self.ui.action_button, 'on_ui_button_press', handler)
        self.event_manager.subscribe(None, 'on_custom_event', handler)

    def on_custom_game_event(self, event):
        if 'event' in event and event['event'] == 'game start':
            self.handle_game_start()

    def join(self):
        host = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('DOMINION_HOST', 'localhost')
        port = os.environ.get('DOMINION_PORT', '55555')
        self.game_client.connect(host, int(port))

    def handle_screen_resize(self, raw_size):
        manager = get_manager()
        width, height = raw_size
        width = min_screen_width if width < min_screen_width else width
        height = min_screen_height if height < min_screen_height else height
        size = (width, height)
        self.surface = pygame.display.set_mode(size, flags=DISPLAY_FLAGS)
        self.ui.window.on_window_size_changed(size)
        manager.set_window_resolution(size)
        manager.root_container.set_dimensions(size)

    def start(self):
        self.game_client.start_game()
        self.handle_game_start()

    def handle_game_start(self):
        self.event_manager.unsubscribe(self.ui.action_button, 'on_ui_button_press')
        self.ui.action_button.set_text('End Turn')
        done_handler = EventHandler()
        done_handler.on_ui_button_press = lambda ui_element: game_client.get_instance().done()
        self.event_manager.subscribe(self.ui.action_button, 'on_ui_button_press', done_handler)

    def handle_event(self, event):
        em = self.event_manager
        mouse_buttons = {
            1: MouseButton.Left,
            2: MouseButton.Middle,
            3: MouseButton.Right,
        }

        if event.type == pygame.MOUSEMOTION:
            em.on_mouse_move(*event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button not in mouse_buttons:
                return
            em.on_mouse_button_down(mouse_buttons[event.button])
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button not in mouse_buttons:
                return
            em.on_mouse_button_up(mouse_buttons[event.button])
        elif event.type == pygame.USEREVENT:
            # handle our custom events
            if event.user_type == 'custom_event':
                em.on_custom_event(event.event)
                return

            # handle pygame GUI's user events
            if not hasattr(event.ui_element, 'owner'):
                return

            ui_element = event.ui_element.owner
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                em.on_ui_button_press(ui_element=ui_element)

    def _handle_message(self, action, data):
        if action == 'play':
            self.player.play()
        elif action == 'respond':
            self.player.pending_response = (action, data)
        elif action == 'on_game_event':
            self.player.on_game_event(data)
        elif action == 'on_state_change':
            self.player.on_state_change(data)
        elif action == 'ack':
            self.name = data['name']
        else:
            print('Unknown message type:', action)

    def update_state(self):
        try:
            message = self.game_client.get_message()
            if message:
                self._handle_message(*message)
        except Exception as e:
            pass

        if self.player is not None and self.player.pending_response is not None:
            _, args = self.player.pending_response
            Responder.get_instance().handle(args['action'], self.player.state, *args['args'])
            self.player.pending_response = None

        if self.player is None or self.player.state == self.state:
            return

        actions = self.player.state['actions']
        buys = self.player.state['buys']
        money = util.calculate_money(self.player.state)
        supply = self.player.state['supply']
        play_area = self.player.state['play_area']
        hand = self.player.state['hand']
        draw_deck = self.player.state['draw_deck']
        discard_pile = self.player.state['discard_pile']

        shop_piles = [util.get_card_name(pile) for pile in supply]
        play_area_cards = [util.get_card_name(card['name']) for card in play_area]
        hand_cards = [util.get_card_name(card['name']) for card in hand]

        disabled_shop_piles = util.filter_card_names(shop_piles, f'card.cost > {money} or {buys == 0}')
        self.ui.shop.disabled_piles = disabled_shop_piles
        self.ui.shop.piles = shop_piles
        self.ui.shop.layout(only_if_changed=False)

        self.ui.play_area.scrollable.cards = play_area_cards
        self.ui.play_area.layout(only_if_changed=False)

        disabled_hand_cards = util.filter_card_names(hand_cards, f'card.type == "Action" and {actions == 0}')
        self.ui.hand.scrollable.disabled_cards = disabled_hand_cards
        self.ui.hand.scrollable.cards = hand_cards
        self.ui.hand.layout(only_if_changed=False)

        self.state = self.player.state

    def main_loop(self, manager, events):
        time_delta = self.clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

            elif event.type == pygame.VIDEORESIZE:
                self.handle_screen_resize(event.dict['size'])

            elif event.type in events:
                self.handle_event(event)

            manager.process_events(event)

        self.update_state()

        try:
            manager.update(time_delta)
        except Exception as e:
            print(f'pygame GUI messed up: {e}')

        self.surface.blit(self.ui.background, (0, 0))
        manager.draw_ui(self.surface)

        pygame.display.update()

    def run(self):
        manager = get_manager()
        mouse_events = (pygame.MOUSEMOTION,
                        pygame.MOUSEBUTTONDOWN,
                        pygame.MOUSEBUTTONUP)
        events = (pygame.USEREVENT,) + mouse_events

        while self.is_running:
            try:
                self.main_loop(manager, events)
            except KeyboardInterrupt:
                self.is_running = False
        pygame.quit()
        self.game_client.shutdown()



if __name__ == '__main__':
    app = DominionApp()
    app.run()
