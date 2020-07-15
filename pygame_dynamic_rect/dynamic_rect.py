from dataclasses import dataclass
from typing import Union

import pygame


@dataclass
class Layout:
    x: Union[int, float]
    y: Union[int, float]
    w: Union[int, float]
    h: Union[int, float]


class Rect(pygame.Rect):
    def __init__(self, container: 'Rect', layout: Layout):
        self.container = container
        self.layout = layout
        self.children = []
        self.calc_rect()
        super().__init__(self.left, self.top, self.width, self.height)

    def calc_rect(self):
        c = self.container
        lo = self.layout
        prev = pygame.Rect(self.topleft, self.size)
        self.left = lo.x if isinstance(lo.x, int) else lo.x * c.width
        self.top = lo.y if isinstance(lo.y, int) else lo.y * c.height
        self.width = lo.w if isinstance(lo.w, int) else lo.w * c.width
        self.height = lo.h if isinstance(lo.h, int) else lo.h * c.height
        if self == prev:
            return
        for child in self.children:
            child.calc_rect()