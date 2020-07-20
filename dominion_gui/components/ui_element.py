from dataclasses import dataclass

from typing import Union
import pygame

from dominion_gui.components.ui_manager import get_manager


@dataclass
class AnchorInfo:
    left: Union[int, float]
    right: Union[int, float]
    top: Union[int, float]
    bottom: Union[int, float]


class UIElement:
    def __init__(self,
                 bounds: [pygame.Rect, None] = None,
                 anchor_info: Union[AnchorInfo, None] = None,
                 container: Union[pygame.Rect, None] = None):
        self._bounds = bounds if bounds else pygame.Rect(0, 0, 0, 0)
        self.anchor_info = anchor_info
        self.container = container
        self.children = []
        self.layout()

    @property
    def manager(self):
        return get_manager()

    @property
    def topleft(self):
        return self._bounds.topleft

    @topleft.setter
    def topleft(self, tl):
        if tl == self._bounds.topleft:
            return
        self._bounds.topleft = tl
        self.layout(only_if_changed=False)

    @property
    def size(self):
        return self._bounds.size

    @size.setter
    def size(self, s):
        if s == self._bounds.size:
            return
        self._bounds.size = s
        self.layout(only_if_changed=False)

    @property
    def width(self):
        return self._bounds.width

    @width.setter
    def width(self, w):
        if w == self._bounds.width:
            return
        self._bounds.width = w
        self.layout(only_if_changed=False)

    @property
    def height(self):
        return self._bounds.height

    @height.setter
    def height(self, h):
        if h == self._bounds.height:
            return
        self._bounds.height = h
        self.layout(only_if_changed=False)

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, b):
        if b == self._bounds:
            return
        self._bounds = b
        self.layout(only_if_changed=False)

    def layout(self, only_if_changed=True):
        if self.container is not None:
            c = self.container
            ai = self.anchor_info
            left = ai.left if isinstance(ai.left, int) else ai.left * c.width
            right = ai.right if isinstance(ai.right, int) else ai.right * c.width
            top = ai.top if isinstance(ai.top, int) else ai.top * c.height
            bottom = ai.bottom if isinstance(ai.bottom, int) else ai.bottom * c.height
            width = self.width if right == -1 else c.width - (left + right)
            height = self.height if bottom == -1 else c.height - (top + bottom)
            new_bounds = pygame.Rect(left, top, width, height)
            if only_if_changed and new_bounds == self.bounds:
                return
            print(self.__class__.__name__, new_bounds)
            self._bounds = new_bounds

        for child in self.children:
            child.layout()
