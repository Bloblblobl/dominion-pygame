import pygame
import pygame_gui

from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.components.card import Card
from dominion_gui.components.default import layout0
from dominion_gui.components.hand import Hand
from dominion_gui.components.message_log import MessageLog
from dominion_gui.event_manager import event_manager
from dominion_gui.ui_elements.button import Button
from dominion_gui.ui_elements.image import Image
from dominion_gui.ui_elements.html_textbox import HTMLTextBox
from layout_info.layout_info import LayoutInfo
from dominion_gui.ui_elements.panel import Panel

from dominion_gui.ui_elements.top_level_window import TopLevelWindow
from dominion_gui.ui_elements.ui_manager import get_manager
from dominion_gui.constants import screen_size, background_color, preloaded_fonts, RED, GREEN, BLUE, YELLOW, DARK_GRAY, \
    min_screen_width, min_screen_height

DISPLAY_FLAGS = pygame.RESIZABLE


class DominionApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dominion')
        self.surface = pygame.display.set_mode(screen_size, flags=DISPLAY_FLAGS)
        self.background = pygame.Surface(screen_size)
        self.clock = pygame.time.Clock()
        self.is_running = True

        # initializing manager
        manager = get_manager(screen_size)
        manager.preload_fonts(preloaded_fonts)

        self.build_ui(screen_size)

    def build_ui(self, screen_size):
        self.background.fill(pygame.Color(background_color))
        # message_log = MessageLog(self.manager)
        # self.side_panel = SidePanel(message_log)
        self.window = TopLevelWindow(screen_size)

        li_all_10 = LayoutInfo(left=10, right=10, top=10, bottom=10)

        gray_panel = Panel(li_all_10, self.window, DARK_GRAY)

        red_li = LayoutInfo(right=20, top=20, bottom=20, width=0.25)
        red_panel = Panel(red_li, self.window, RED)

        text_li = LayoutInfo(left=0, right=0, top=0, height=0.8)
        self.message_log = MessageLog(text_li, red_panel, padding=li_all_10)

        button1_li = LayoutInfo(left=0, right=0, top=0.8, height=0.1)
        button1_pad = LayoutInfo(left=10, right=10, top=0, bottom=10)
        button1_text = 'Start Game'
        button1 = Button(button1_text, button1_li, red_panel, padding=button1_pad)
        button_eh = BaseEventHandler()
        button_eh.on_ui_button_pressed = lambda ui_element: print('Hooray! It works!', ui_element)
        event_manager.subscribe(button1, pygame_gui.UI_BUTTON_PRESSED, button_eh)
        event_manager.subscribe(button1, pygame_gui.UI_BUTTON_PRESSED, button_eh)

        button2_li = LayoutInfo(left=0, right=0, top=0.9, height=0.1)
        button2_pad = LayoutInfo(left=10, right=10, top=0, bottom=10)
        button2_text = 'End Turn'
        button2 = Button(button2_text, button2_li, red_panel, padding=button2_pad)

        green_li = LayoutInfo(left=20, right=30.25, top=0.7, bottom=20)
        green_panel = Panel(green_li, self.window, GREEN)

        blue_panel = Panel(li_all_10, green_panel, BLUE)

        # card_li = LayoutInfo(left=10, top=10, bottom=10, width=0.2)
        # card = Card('artisan', card_li, blue_panel, count=35)

        hand = Hand(layout0, blue_panel)
        hand.cards = ['artisan', 'bandit', 'bureaucrat', 'copper', 'festival']

        yellow_li = LayoutInfo(left=20, right=30.25, top=20, bottom=10.3)
        yellow_panel = Panel(yellow_li, self.window, YELLOW)

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

    def run(self):
        manager = get_manager()
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.VIDEORESIZE:
                    self.handle_screen_resize(event.dict['size'])

                if event.type == pygame.USEREVENT:
                    event_manager.handle_event(event)

                manager.process_events(event)

            manager.update(time_delta)

            self.surface.blit(self.background, (0, 0))
            manager.draw_ui(self.surface)

            pygame.display.update()


if __name__ == '__main__':
    app = DominionApp()
    app.run()
