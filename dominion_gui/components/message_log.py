import pygame

from pygame_gui.elements import UIPanel, UILabel, UITextBox
from dominion_gui.constants import screen_width, screen_height

log_text = ['<b>[Event]</b> <font color=#FF5CC9>WARNING!</font> Player 1 drew a card!',
            '<b>[Event]</b> Player 2 drew a card!<br>'] * 20


class MessageLog:
    def __init__(self, manager):
        self.log_text = log_text
        panel_size = panel_width, panel_height = 300, screen_height - 20
        panel_pos = (screen_width - panel_width - 10, 10)
        self.panel = UIPanel(relative_rect=pygame.Rect(panel_pos, panel_size),
                             starting_layer_height=2,
                             manager=manager)

        label_size = label_width, label_height = (100, 20)
        label_pos = (0, 10)
        self.label = UILabel(relative_rect=pygame.Rect(label_pos, label_size),
                        text='Sidepanel',
                        manager=manager,
                        container=self.panel)

        log_size = (panel_width - 20, panel_height - 50)
        log_pos = (7, 40)
        transformed_text = '<br>'.join(self.log_text)
        self.log = UITextBox(relative_rect=pygame.Rect(log_pos, log_size),
                        html_text=transformed_text,
                        manager=manager,
                        container=self.panel)
