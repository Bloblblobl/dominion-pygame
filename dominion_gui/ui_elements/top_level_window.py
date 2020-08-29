import pygame

from dominion_gui.ui_elements.ui_element import UIElement


class TopLevelWindow(pygame.Rect, UIElement):
    def __init__(self, screen_size):
        super().__init__((0, 0), screen_size)
        UIElement.__init__(self)
        self.children = []

    def on_window_size_changed(self, new_size):
        self.size = new_size
        for child in self.children:
            child.layout()
