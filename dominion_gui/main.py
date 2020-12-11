import os

import pygame
import pygame_gui


from dominion_gui import game_client, util
from dominion_gui.event_handler import EventHandler, MouseButton
from dominion_gui.constants import screen_size, preloaded_fonts, min_screen_width, min_screen_height, \
    DISPLAY_FLAGS
import dominion_gui.event_manager as em
from dominion_gui.ui_manager import get_manager
from dominion_gui.ui_factory import UI
from dominion_gui.ui_player import UIPlayer


class DominionApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dominion')
        self.surface = pygame.display.set_mode(screen_size, flags=DISPLAY_FLAGS)
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.event_manager = None
        self.player = None
        self.state = None

        manager = get_manager(screen_size)
        manager.preload_fonts(preloaded_fonts)

        self.ui = UI()
        self.connect_events()

    def connect_events(self):
        self.event_manager = em.get_event_manager(self.ui.window)
        button_top_eh = EventHandler()
        button_top_eh.on_ui_button_press = lambda ui_element: self.connect()
        button_bottom_eh = EventHandler()
        button_bottom_eh.on_ui_button_press = lambda ui_element: game_client.get_instance().done()
        self.event_manager.subscribe(self.ui.top_button, 'on_ui_button_press', button_top_eh)
        self.event_manager.subscribe(self.ui.bottom_button, 'on_ui_button_press', button_bottom_eh)

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
        host = os.environ.get('DOMINION_HOST', 'locahost')
        port = os.environ.get('DOMINION_PORT', '50051')
        game_client.connect(host, int(port))
        self.player = UIPlayer.instance

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

    def update_state(self):
        if self.player is None or self.player.state == self.state:
            return

        supply = self.player.state['supply']
        play_area = self.player.state['play_area']
        hand = self.player.state['hand']
        draw_deck = self.player.state['draw_deck']
        discard_pile = self.player.state['discard_pile']

        shop_piles = [util.get_card_name(pile) for pile in supply]
        play_area_cards = [util.get_card_name(card['name']) for card in play_area]
        hand_cards = [util.get_card_name(card['name']) for card in hand]

        self.ui.shop.piles = shop_piles
        self.ui.play_area.scrollable.cards = play_area_cards
        self.ui.play_area.layout(only_if_changed=False)
        self.ui.hand.scrollable.cards = hand_cards
        self.ui.hand.layout(only_if_changed=False)
        self.state = self.player.state

    def run(self):
        manager = get_manager()
        mouse_events = (pygame.MOUSEMOTION,
                        pygame.MOUSEBUTTONDOWN,
                        pygame.MOUSEBUTTONUP)
        events = (pygame.USEREVENT,) + mouse_events

        while self.is_running:
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


if __name__ == '__main__':
    app = DominionApp()
    app.run()
