import pygame
import pygame_gui

from dominion_gui.components.ui_element import AnchorInfo
from dominion_gui.components.ui_panel import UIPanel

from dominion_gui.components.side_panel import SidePanel
from dominion_gui.components.message_log import MessageLog
from dominion_gui.components.top_level_window import TopLevelWindow
from dominion_gui.components.ui_manager import get_manager
from dominion_gui.constants import screen_size, background_color, preloaded_fonts, RED, GREEN
from pygame_dynamic_rect.dynamic_rect import Rect, Layout


class DominionApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dominion')
        self.surface = pygame.display.set_mode(screen_size, flags=pygame.RESIZABLE)
        self.background = pygame.Surface(screen_size)
        self.clock = pygame.time.Clock()
        self.is_running = True

        # inititalizing manager
        manager = get_manager(screen_size)
        manager.preload_fonts(preloaded_fonts)

        self.build_ui(screen_size)

    def build_ui(self, screen_size):
        manager = get_manager()
        self.background.fill(pygame.Color(background_color))
        # message_log = MessageLog(self.manager)
        # self.side_panel = SidePanel(message_log)
        self.window = TopLevelWindow(screen_size)
        red_ai = AnchorInfo(0.1, 0.1, 0.1, 0.8)
        self.red_panel = UIPanel(red_ai, self.window, RED)
        green_ai = AnchorInfo(0.1, 0.1, 200, 200)
        self.green_panel = UIPanel(green_ai, self.window, GREEN)

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
