from typing import Union
import pygame

from layout_info.layout_info import LayoutInfo
from dominion_gui.components.ui_manager import get_manager


class UIElement:
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, None] = None):
        if not layout_info.is_valid:
            raise Exception('Invalid layout')

        self._bounds = pygame.Rect(0, 0, 0, 0)
        self.layout_info = layout_info
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
    def left(self):
        return self._bounds.left

    @left.setter
    def left(self, l):
        if l == self._bounds.left:
            return
        self._bounds.left = l
        self.layout(only_if_changed=False)

    @property
    def top(self):
        return self._bounds.top

    @top.setter
    def top(self, t):
        if t == self._bounds.top:
            return
        self._bounds.top = t
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

    @property
    def absolute_rect(self):
        c = self.container
        if c is None:
            return self._bounds
        left, top, width, height = self.layout_info.get_absolute_rect(c.size)
        left += c.absolute_rect.left if isinstance(c, UIElement) else c.left
        top += c.absolute_rect.top if isinstance(c, UIElement) else c.top
        return pygame.Rect(left, top, width, height)

    def layout(self, only_if_changed=True):
        if self.container is not None:
            new_bounds = self.absolute_rect
            if only_if_changed and new_bounds == self.bounds:
                return
            print(self.__class__.__name__, new_bounds)
            self._bounds = new_bounds

        for child in self.children:
            child.layout()
