import pygame
import pygame_gui
import time
from dominion_grpc_client.client import Client as GRPCClient
from threading import Thread

from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.constants import screen_size, preloaded_fonts, min_screen_width, min_screen_height, \
    DISPLAY_FLAGS
import dominion_gui.event_manager as em
from dominion_gui.ui_elements.ui_manager import get_manager
from dominion_gui.ui_factory import UI
from ui_player import UIPlayer


class DominionApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dominion')
        self.surface = pygame.display.set_mode(screen_size, flags=DISPLAY_FLAGS)
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.event_manager = None
        self.client = None
        self.player = None

        manager = get_manager(screen_size)
        manager.preload_fonts(preloaded_fonts)

        self.ui = UI()
        self.connect_events()

    def connect_events(self):
        self.event_manager = em.get_event_manager(self.ui.window)
        button_eh = BaseEventHandler()
        button_eh.on_ui_button_pressed = lambda ui_element: self.connect()
        self.event_manager.subscribe(self.ui.top_button, pygame_gui.UI_BUTTON_PRESSED, button_eh)

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

    def connect(self):
        self.client = GRPCClient('test', UIPlayer)
        self.player = UIPlayer.instance

        Thread(target=self.client.run).start()
        game_started = False
        while not game_started:
            try:
                self.client.start_game()
                game_started = True
            except:
                time.sleep(0.1)

    def run(self):
        manager = get_manager()
        prev_state = None
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                elif event.type == pygame.VIDEORESIZE:
                    self.handle_screen_resize(event.dict['size'])

                elif event.type in self.event_manager.events:
                    self.event_manager.handle_event(event)

                manager.process_events(event)

            if self.player is not None and self.player.state != prev_state:
                supply = self.player.state['supply']
                play_area = self.player.state['play_area']
                hand = self.player.state['hand']
                draw_deck = self.player.state['draw_deck']
                discard_pile = self.player.state['discard_pile']

                shop_piles = [pile.lower() for pile in supply]
                play_area_cards = [card['name'].lower() for card in play_area]
                hand_cards = [card['name'].lower() for card in hand]

                self.ui.shop.piles = shop_piles
                self.ui.play_area.scrollable.cards = play_area_cards
                self.ui.play_area.layout(only_if_changed=False)
                self.ui.hand.scrollable.cards = hand_cards
                em.first_card = self.ui.hand.scrollable.cards[0]
                self.ui.hand.layout(only_if_changed=False)
                prev_state = self.player.state

            manager.update(time_delta)

            self.surface.blit(self.ui.background, (0, 0))
            manager.draw_ui(self.surface)

            pygame.display.update()


if __name__ == '__main__':
    app = DominionApp()
    app.run()
