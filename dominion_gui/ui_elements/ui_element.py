from typing import Union
import pygame

from layout_info.layout_info import LayoutInfo
from dominion_gui.ui_elements.ui_manager import get_manager


class UIElement:
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union['UIElement', None] = None,
                 padding: Union[LayoutInfo, None] = None,
                 enabled: bool = True):
        self._bounds = pygame.Rect(0, 0, 0, 0)
        self._element = None
        self._visible = True
        self.layout_info = layout_info
        self.container = container
        self.padding = padding
        self.children = []
        self.enabled = enabled

        if self.layout_info is None:
            self.layout_info = LayoutInfo(0, 0, 0, 0)
        if not self.layout_info.is_valid:
            raise Exception('Invalid layout')
        if self.container is not None:
            self.container.children.append(self)

        self.layout()
        self._validate_padding()

    def _validate_padding(self):
        p = self.padding
        if p is not None and (not p.is_valid or p.width is not None or p.height is not None):
            raise Exception('Invalid padding')

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, value):
        self._element = value
        self._element.owner = self

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
    def content_size(self):
        return self.size

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
    def padded_rect(self):
        c = self.container
        if c is None:
            return self._bounds
        left, top, width, height = self.layout_info.get_absolute_rect(c.size)
        left += c.padded_rect.left if isinstance(c, UIElement) else c.left
        top += c.padded_rect.top if isinstance(c, UIElement) else c.top

        if self.padding is not None:
            pleft, ptop, width, height = self.padding.get_absolute_rect((width, height))
            left += pleft
            top += ptop

        return pygame.Rect(left, top, width, height)

    def _on_enable(self, enabled: bool):
        pass

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        self._enabled = enabled
        self._on_enable(enabled)

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible
        if visible:
            self.show()
        else:
            self.hide()

    def hide(self):
        if self.element is not None:
            self.element.hide()

    def show(self):
        if self.element is not None:
            self.element.show()

    def rebuild(self):
        self.element.set_position(self.topleft)
        self.element.set_dimensions(self.size)
        self.element.rebuild()

    def layout(self, only_if_changed=True):
        if self.container is not None:
            new_bounds = self.padded_rect
            if only_if_changed and new_bounds == self.bounds:
                return
            self._bounds = new_bounds

        for child in self.children:
            child.layout(only_if_changed)

        if self.element is not None:
            self.rebuild()
