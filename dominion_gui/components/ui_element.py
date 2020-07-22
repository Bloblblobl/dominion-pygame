from dataclasses import dataclass

from typing import Union
import pygame

from dominion_gui.components.ui_manager import get_manager


@dataclass
class LayoutInfo:
    left: Union[int, float, None]
    right: Union[int, float, None]
    top: Union[int, float, None]
    bottom: Union[int, float, None]
    width: Union[int, float, None]
    height: Union[int, float, None]

    @property
    def is_valid(self):
        x_dimension = [self.left, self.right, self.width]
        y_dimension = [self.top, self.bottom, self.height]

        return x_dimension.count(None) == 1 and y_dimension.count(None) == 1

    def get_absolute_rect(self, container: pygame.Rect):
        cw = container.width
        ch = container.height
        l, r, t, b, = self.left, self.right, self.top, self.bottom
        w, h = self.width, self.height

        l = int(l * cw) if isinstance(l, float) else l
        r = int(r * cw) if isinstance(r, float) else r
        t = int(t * ch) if isinstance(t, float) else t
        b = int(b * ch) if isinstance(b, float) else b
        w = int(w * cw) if isinstance(w, float) else w
        h = int(h * ch) if isinstance(h, float) else h

        if w is not None:
            left = l if l is not None else cw - w - r
            width = w
        else:
            left = l
            width = cw - l - r

        if h is not None:
            top = t if t is not None else ch - h - b
            height = h
        else:
            top = t
            height = ch - t - b

        return pygame.Rect(left, top, width, height)

class UIElement:
    def __init__(self,
                 bounds: [pygame.Rect, None] = None,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, None] = None):
        if not layout_info.is_valid:
            raise Exception('Invalid layout')

        self._bounds = bounds if bounds else pygame.Rect(0, 0, 0, 0)
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
            new_bounds = self.layout_info.get_absolute_rect(self.container)
            if only_if_changed and new_bounds == self.bounds:
                return
            print(self.__class__.__name__, new_bounds)
            self._bounds = new_bounds

        for child in self.children:
            child.layout()
