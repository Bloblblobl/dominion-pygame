import pygame
import pygame_gui

from dominion_gui.components.button import Button
from dominion_gui.components.textbox import TextBox
from layout_info.layout_info import LayoutInfo
from dominion_gui.components.panel import Panel

from dominion_gui.components.top_level_window import TopLevelWindow
from dominion_gui.components.ui_manager import get_manager
from dominion_gui.constants import screen_size, background_color, preloaded_fonts, RED, GREEN, BLUE, YELLOW, DARK_GRAY


class DominionApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dominion')
        self.surface = pygame.display.set_mode(screen_size, flags=pygame.RESIZABLE)
        self.background = pygame.Surface(screen_size)
        self.clock = pygame.time.Clock()
        self.is_running = True

        # initializing manager
        manager = get_manager(screen_size)
        manager.preload_fonts(preloaded_fonts)

        self.build_ui(screen_size)

    def build_ui(self, screen_size):
        #manager = get_manager()
        self.background.fill(pygame.Color(background_color))
        # message_log = MessageLog(self.manager)
        # self.side_panel = SidePanel(message_log)
        self.window = TopLevelWindow(screen_size)

        padding = LayoutInfo(left=10, right=10, top=10, bottom=10)

        gray_li = LayoutInfo(left=10, right=10, top=10, bottom=10)
        gray_panel = Panel(gray_li, self.window, DARK_GRAY)

        red_li = LayoutInfo(right=20, top=20, bottom=20, width=0.25)
        red_panel = Panel(red_li, self.window, RED)

        text_li = LayoutInfo(left=0, right=0, top=0, height=0.8)
        text_pad = LayoutInfo(left=10, right=10, top=10, bottom=10)
        text = '[Player 1] played a card<br>' \
               '[Player 2] discarded a card<br>' \
               '' * 100
        textbox = TextBox(text, text_li, red_panel, padding=text_pad)

        button1_li = LayoutInfo(left=0, right=0, top=0.8, height=0.1)
        button1_pad = LayoutInfo(left=10, right=10, top=0, bottom=10)
        button1_text = 'Start Game'
        button1 = Button(button1_text, button1_li, red_panel, padding=button1_pad)

        button2_li = LayoutInfo(left=0, right=0, top=0.9, height=0.1)
        button2_pad = LayoutInfo(left=10, right=10, top=0, bottom=10)
        button2_text = 'End Turn'
        button2 = Button(button2_text, button2_li, red_panel, padding=button2_pad)

        green_li = LayoutInfo(left=20, right=30.25, top=0.7, bottom=20)
        green_panel = Panel(green_li, self.window, GREEN)

        blue_li = LayoutInfo(left=10, right=10, top=10, bottom=10)
        blue_panel = Panel(blue_li, green_panel, BLUE)

        yellow_li = LayoutInfo(left=20, right=30.25, top=20, bottom=10.3)
        yellow_panel = Panel(yellow_li, self.window, YELLOW)

    def run(self):
        manager = get_manager()
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.VIDEORESIZE:
                    size = event.dict['size']
                    self.window.on_window_size_changed(size)
                    manager.set_window_resolution(size)
                    manager.root_container.set_dimensions(size)

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # if event.ui_element == hello_button:
                        #     print('Hello World!')
                        pass

                manager.process_events(event)

            manager.update(time_delta)

            self.surface.blit(self.background, (0, 0))
            manager.draw_ui(self.surface)

            pygame.display.update()


if __name__ == '__main__':
    app = DominionApp()
    app.run()
