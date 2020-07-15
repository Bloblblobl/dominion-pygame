import pygame

from pygame_dynamic_rect.dynamic_rect import Rect, Layout


class TopLevelWindow:
    def __init__(self, screen_size):
        container = pygame.Rect((0, 0), screen_size)
        self.rect = Rect(container, Layout(0, 0, 1.0, 1.0))

    def on_window_size_changed(self, new_size):
        self.rect.container.size = new_size
        self.rect.calc_rect()
