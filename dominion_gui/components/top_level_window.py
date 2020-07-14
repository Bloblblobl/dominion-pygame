import pygame

from pygame_dynamic_rect.dynamic_rect import Rect


class TopLevelWindow:
    def __init__(self, screen_size):
        container = pygame.Rect((0, 0), screen_size)
        rect = pygame.Rect((0, 0), (100, 100))
        self.rect = Rect(container, percent_rect=rect)

    def on_window_size_changed(self, new_size):
        self.rect.container.size = new_size
        self.rect.calc_rect()