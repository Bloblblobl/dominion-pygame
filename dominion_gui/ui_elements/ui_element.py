import pygame

from dominion_gui.event_manager import get_event_manager
from dominion_gui.ui_manager import get_manager
from dominion_gui.util import Noneable
from layout_info.layout_info import LayoutInfo


class UIElement:
    def __init__(self,
                 layout_info: Noneable(LayoutInfo) = None,
                 container: Noneable('UIElement') = None,
                 padding: Noneable(LayoutInfo) = None,
                 enabled: bool = True):
        self._event_manager = self._get_event_manager()

        self._bounds = pygame.Rect(0, 0, 0, 0)
        self._container = None
        self._element = None
        self._visible = True
        self.layout_info = layout_info
        self.container = container
        self.padding = padding
        self.children = []
        self.enabled = enabled
        # participates in Mouse Enter and Mouse Leave events
        self.mouse_target = True

        if self.layout_info is None:
            self.layout_info = LayoutInfo(0, 0, 0, 0)
        if not self.layout_info.valid:
            raise Exception('Invalid layout')

        self.layout()
        self._validate_padding()

    def _get_event_manager(self):
        return get_event_manager()

    def _validate_padding(self):
        p = self.padding
        if p is not None and (not p.valid or p.width is not None or p.height is not None):
            raise Exception('Invalid padding')

    def subscribe(self, *args, **kwargs):
        self._event_manager.subscribe(*args, **kwargs)

    def unsubscribe(self, *args, **kwargs):
        self._event_manager.unsubscribe(*args, **kwargs)

    def add_child(self, child: 'UIElement'):
        if child in self.children:
            raise Exception(f'Child already exists {child}')
        self.children.append(child)

    @property
    def element(self):
        return self._element

    @element.setter
    def element(self, value):
        self._element = value
        self._element.owner = self

    @property
    def container(self):
        return self._container

    @container.setter
    def container(self, c):
        if c is not None:
            if self._container is not None:
                self._container.children.remove(self)
            c.add_child(self)
        self._container = c

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
    def right(self):
        return self._bounds.right

    @right.setter
    def right(self, r):
        if r == self._bounds.right:
            return
        self._bounds.right = r
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
    def bottom(self):
        return self._bounds.bottom

    @bottom.setter
    def bottom(self, b):
        if b == self._bounds.bottom:
            return
        self._bounds.bottom = b
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

    def on_enable(self, enabled: bool):
        if self.element is None:
            return

        if enabled:
            self.element.enable()
        else:
            self.element.disable()

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        self._enabled = enabled
        self.on_enable(enabled)

    def on_visible(self, visible: bool):
        for child in self.children:
            child.visible = visible

        if self.element is None:
            return

        if visible:
            self.element.show()
        else:
            self.element.hide()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, visible: bool):
        self._visible = visible
        self.on_visible(visible)

    def kill(self):
        if self.element is not None:
            self.element.kill()

        for child in self.children:
            child.kill()

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
