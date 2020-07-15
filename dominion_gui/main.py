import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel

from dominion_gui.components.side_panel import SidePanel
from dominion_gui.components.message_log import MessageLog
from dominion_gui.components.top_level_window import TopLevelWindow
from dominion_gui.constants import screen_size, background_color, preloaded_fonts
from pygame_dynamic_rect.dynamic_rect import Rect, Layout


class DominionApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dominion')
        self.surface = pygame.display.set_mode(screen_size, flags=pygame.RESIZABLE)
        self.background = pygame.Surface(screen_size)
        self.manager = UIManager(screen_size)
        self.manager.preload_fonts(preloaded_fonts)
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.build_ui(screen_size)

    def build_ui(self, screen_size):
        self.background.fill(pygame.Color(background_color))
        # message_log = MessageLog(self.manager)
        # self.side_panel = SidePanel(message_log)
        self.window = TopLevelWindow(screen_size)
        red_rect = Rect(self.window.rect, Layout(.6, .6, .3, 100))
        green_rect = Rect(self.window.rect,Layout(.2, .2, 100, .3))
        self.window.rect.children += [red_rect, green_rect]

        self.panel = UIPanel(self.window.rect, 1, self.manager)
        self.red_panel = UIPanel(red_rect, 2, self.manager)
        self.red_panel.background_colour = pygame.Color(255, 0, 0)
        self.red_panel.rebuild()
        self.green_panel = UIPanel(green_rect, 3, self.manager)
        self.green_panel.background_colour = pygame.Color(0, 255, 0)
        self.green_panel.rebuild()


    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.VIDEORESIZE:
                    size = event.dict['size']
                    self.window.on_window_size_changed(size)
                    self.manager.set_window_resolution(size)
                    self.manager.root_container.set_dimensions(size)
                    self.panel.set_dimensions(size)
                    self.panel.rebuild()
                    new_red_rect = self.window.rect.children[0]
                    self.red_panel.set_position(new_red_rect.topleft)
                    self.red_panel.set_dimensions(new_red_rect.size)
                    self.red_panel.rebuild()
                    new_green_rect = self.window.rect.children[1]
                    self.green_panel.set_position(new_green_rect.topleft)
                    self.green_panel.set_dimensions(new_green_rect.size)
                    self.green_panel.rebuild()

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        # if event.ui_element == hello_button:
                        #     print('Hello World!')
                        pass

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.surface)

            pygame.display.update()


if __name__ == '__main__':
    app = DominionApp()
    app.run()
