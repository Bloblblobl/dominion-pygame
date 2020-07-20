import pygame


class TopLevelWindow(pygame.Rect):
    def __init__(self, screen_size):
        super().__init__((0, 0), screen_size)
        self.children = []

    def on_window_size_changed(self, new_size):
        print('TopLevelWindow(), size:', new_size)
        self.size = new_size
        for child in self.children:
            child.layout()
