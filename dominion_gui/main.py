import pygame
import pygame_gui
from pygame_gui import UIManager
from pygame_gui.elements import UIPanel, UILabel, UITextBox

from dominion_gui.constants import screen_size, screen_width, screen_height, background_color, preloaded_fonts


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
        panel_size = panel_width, panel_height = 300, screen_height - 20
        panel_pos = (screen_width - panel_width - 10, 10)
        panel = UIPanel(relative_rect=pygame.Rect(panel_pos, panel_size),
                        starting_layer_height=2,
                        manager=self.manager)

        label_size = label_width, label_height = (100, 20)
        label_pos = (0, 10)
        label = UILabel(relative_rect=pygame.Rect(label_pos, label_size),
                        text='Sidepanel',
                        manager=self.manager,
                        container=panel)

        log_text = '<b>[Event]</b> <font color=#FF5CC9>WARNING!</font> Player 1 drew a card!<br>' \
                   '<b>[Event]</b> Player 2 drew a card!<br>' * 20
        log_size = (panel_width - 20, panel_height - 50)
        log_pos = (7, 40)
        log = UITextBox(relative_rect=pygame.Rect(log_pos, log_size),
                        html_text=log_text,
                        manager=self.manager,
                        container=panel)

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
