import pygame
import pygame_gui
from pygame_gui import UIManager

from dominion_gui.components.side_panel import SidePanel
from dominion_gui.components.message_log import MessageLog
from dominion_gui.constants import screen_size, background_color, preloaded_fonts


class DominionApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Dominion')
        self.surface = pygame.display.set_mode(screen_size)
        self.background = pygame.Surface(screen_size)
        self.manager = UIManager(screen_size)
        self.manager.preload_fonts(preloaded_fonts)
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.build_ui()

    def build_ui(self):
        self.background.fill(pygame.Color(background_color))
        message_log = MessageLog(self.manager)
        self.side_panel = SidePanel(message_log)

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

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
