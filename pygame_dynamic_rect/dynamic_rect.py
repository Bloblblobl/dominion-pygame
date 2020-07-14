import pygame


def default_rect():
    return pygame.Rect(-1, -1, -1, -1)


class Rect(pygame.Rect):
    def __init__(self,
                 container,
                 absolute_rect=default_rect(),
                 percent_rect=default_rect()):
        self.container = container
        self.absolute_rect = absolute_rect
        self.percent_rect = percent_rect
        self.children = []
        self.calc_rect()
        super().__init__(self.left, self.top, self.width, self.height)

    def calc_rect(self):
        c = self.container
        ar = self.absolute_rect
        pr = self.percent_rect
        prev = pygame.Rect(self.topleft, self.size)
        self.left = ar.left if ar.left != -1 else pr.left * c.width / 100
        self.top = ar.top if ar.top != -1 else pr.top * c.height / 100
        self.width = ar.width if ar.width != -1 else pr.width * c.width / 100
        self.height = ar.height if ar.height != -1 else pr.height * c.height / 100
        if self == prev:
            return
        for child in self.children:
            child.calc_rect()