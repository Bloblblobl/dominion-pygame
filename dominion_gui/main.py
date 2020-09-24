import time

from threading import Thread

import pygame
import pygame_gui
from dominion_grpc_client.client import Client as GRPCClient

from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.components.card_view import CardView
from dominion_gui.components.default import get_default_layout
from dominion_gui.components.message_log import MessageLog
from dominion_gui.components.shop import Shop
from dominion_gui.constants import screen_size, background_color, preloaded_fonts, min_screen_width, min_screen_height, \
    DISPLAY_FLAGS, Colors
from dominion_gui.event_manager import get_event_manager
from dominion_gui.ui_elements.button import Button
from dominion_gui.ui_elements.horizontal_scroll_container import HorizontalScrollContainer
from dominion_gui.ui_elements.panel import Panel
from dominion_gui.ui_elements.top_level_window import TopLevelWindow
from dominion_gui.ui_elements.ui_manager import get_manager
from layout_info.layout_info import LayoutInfo
from ui_player import UIPlayer


class DominionApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dominion')
        self.surface = pygame.display.set_mode(screen_size, flags=DISPLAY_FLAGS)
        self.background = pygame.Surface(screen_size)
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.event_manager = None
        self.client = None
        self.player = None

        # initializing manager
        manager = get_manager(screen_size)
        manager.preload_fonts(preloaded_fonts)

        self.build_ui(screen_size)

    def build_ui(self, screen_size):
        self.background.fill(background_color)
        # message_log = MessageLog(self.manager)
        # self.side_panel = SidePanel(message_log)
        self.window = TopLevelWindow(screen_size)
        self.event_manager = get_event_manager(self.window)

        li_all_10 = LayoutInfo(left=10, right=10, top=10, bottom=10)

        gray_panel = Panel(li_all_10, self.window, Colors.BORDER)

        red_li = LayoutInfo(right=20, top=20, bottom=20, width=0.25)
        red_panel = Panel(red_li, gray_panel, Colors.SIDE_PANEL)

        text_li = LayoutInfo(left=0, right=0, top=0, height=0.8)
        self.message_log = MessageLog(text_li, red_panel, padding=li_all_10)

        button1_li = LayoutInfo(left=0, right=0, top=0.8, height=0.1)
        button1_pad = LayoutInfo(left=10, right=10, top=0, bottom=10)
        button1_text = 'Start Game'
        button1 = Button(text=button1_text,
                         layout_info=button1_li,
                         container=red_panel,
                         padding=button1_pad,
                         corner_radius_ratio=0.2)
        button_eh = BaseEventHandler()
        button_eh.on_ui_button_pressed = lambda ui_element: self.connect()
        self.event_manager.subscribe(button1, pygame_gui.UI_BUTTON_PRESSED, button_eh)

        button2_li = LayoutInfo(left=0, right=0, top=0.9, height=0.1)
        button2_pad = LayoutInfo(left=10, right=10, top=0, bottom=10)
        button2_text = 'End Turn'
        button2 = Button(text=button2_text,
                         layout_info=button2_li,
                         container=red_panel,
                         padding=button2_pad,
                         corner_radius_ratio=0.2)

        green_li = LayoutInfo(left=20, right=30.25, top=0.7, bottom=20)
        green_panel = Panel(green_li, gray_panel, Colors.HAND_BORDER)

        blue_panel = Panel(li_all_10, green_panel, Colors.HAND)

        # self.test_content_calc(blue_panel)

        hand = HorizontalScrollContainer(get_default_layout(), blue_panel, CardView, 0.035)
        # scroll_container.scrollable.cards = ['artisan', 'bandit', 'bureaucrat', 'copper', 'festival', 'artisan', 'bandit', 'bureaucrat', 'artisan', 'bandit', 'bureaucrat', 'copper', 'festival', 'artisan', 'bandit', 'bureaucrat']
        hand.scrollable.cards = ['artisan', 'bandit', 'bureaucrat', 'copper', 'festival', 'artisan', 'bandit',
                                 'bureaucrat']
        # scroll_container.scrollable.cards = ['artisan', 'bandit', 'bureaucrat']
        hand.layout(only_if_changed=False)

        yellow_li = LayoutInfo(left=20, right=30.25, top=20, bottom=10.3)
        yellow_panel = Panel(yellow_li, gray_panel, Colors.STORE)

        shop_li = LayoutInfo(left=0, right=0, top=0, height=0.5)
        shop = Shop(shop_li, yellow_panel)
        # shop.piles = ['bandit']
        shop.piles = ['artisan', 'bandit', 'bureaucrat', 'festival', 'councilroom', 'estate', 'duchy', 'province',
                      'curse', 'market', 'gardens', 'smithy', 'militia', 'laboratory', 'copper', 'silver', 'gold']

        play_area_li = LayoutInfo(left=0, right=0, bottom=0, height=0.5)
        play_area = HorizontalScrollContainer(play_area_li, yellow_panel, CardView, 0.035)
        play_area.scrollable.cards = ['artisan', 'bandit', 'bureaucrat', 'copper', 'festival', 'artisan', 'bandit',
                                      'bureaucrat']
        play_area.layout(only_if_changed=False)

    def handle_screen_resize(self, raw_size):
        manager = get_manager()
        width, height = raw_size
        width = min_screen_width if width < min_screen_width else width
        height = min_screen_height if height < min_screen_height else height
        size = (width, height)
        self.surface = pygame.display.set_mode(size, flags=DISPLAY_FLAGS)
        self.window.on_window_size_changed(size)
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

            manager.update(time_delta)

            self.surface.blit(self.background, (0, 0))
            manager.draw_ui(self.surface)

            pygame.display.update()


if __name__ == '__main__':
    app = DominionApp()
    app.run()
