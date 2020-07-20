import copy

import pygame

from dominion_gui.components.ui_element import UIElement, AnchorInfo
from pygame_dynamic_rect.dynamic_rect import Rect, Layout


class TopLevelWindow(pygame.Rect):
    def __init__(self, screen_size):
        super().__init__((0, 0), screen_size)
        self.children = []

    def on_window_size_changed(self, new_size):
        self.size = new_size
        for child in self.children:
            child.layout()
