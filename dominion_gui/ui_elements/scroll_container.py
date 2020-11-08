from enum import Enum

import pygame
from typing import Callable

import pygame_gui

from dominion_gui.event_handler import EventHandler
from dominion_gui.components.default import get_default_layout
from dominion_gui.constants import RED
from dominion_gui.event_manager import get_event_manager
from dominion_gui.ui_elements.panel import Panel
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class ScrollbarPosition(Enum):
    LEFT = 1
    RIGHT = 2
    TOP = 3
    BOTTOM = 4


class ScrollThumb(Panel):
    def __init__(self,
                 layout_info: LayoutInfo,
                 scrollbar: UIElement,
                 get_content_size_func: Callable,
                 get_offset_func: Callable,
                 background_color: pygame.Color = None,
                 padding: LayoutInfo = None,
                 depth: int = 0,
                 corner_radius: int = None):
        self.get_content_size = get_content_size_func
        self.get_offset = get_offset_func
        self.ratio = 0.0
        super().__init__(layout_info, scrollbar, background_color, padding, depth, corner_radius)

    def layout(self, only_if_changed=True):
        content_width, content_height = self.get_content_size()
        offset = self.get_offset()
        if self.container.orientation == Orientation.HORIZONTAL:
            self.ratio = 0.0 if content_width == 0 else self.container.width / content_width
            self.layout_info.width = int(self.ratio * self.container.width)
            self.layout_info.left = offset
        else:
            self.ratio = 0.0 if content_height == 0 else self.container.height / content_height
            self.layout_info.height = int(self.ratio * self.container.height)
            self.layout_info.top = offset
        super().layout(only_if_changed)


class Scrollbar(UIElement):
    def __init__(self,
                 layout_info: LayoutInfo,
                 container: UIElement,
                 orientation: Orientation):
        self.orientation = orientation
        self.offset = 0
        super().__init__(layout_info, container)
        self.thumb = ScrollThumb(get_default_layout(),
                                 self,
                                 lambda: self.container.scrollable.content_size,
                                 lambda: self.container.scrollable.offset,
                                 RED)

    def hide(self):
        self.thumb.hide()

    def show(self):
        self.thumb.show()


class ScrollContainer(UIElement, EventHandler):
    def __init__(self,
                 layout_info: LayoutInfo,
                 container: UIElement,
                 scrollable_class,
                 scrollbar_position: ScrollbarPosition,
                 scrollbar_thickness: int,
                 padding: LayoutInfo = None):
        self.scrollable = None
        self.scrollable_class = scrollable_class
        self.scrollbar = None
        self.scrollbar_position = scrollbar_position
        self.scrollbar_thickness = scrollbar_thickness

        super().__init__(layout_info, container, padding)

        get_event_manager().subscribe(self.scrollbar, pygame_gui.UI_HORIZONTAL_SLIDER_MOVED, self.scrollable)

    def _configure(self):
        if self.scrollbar_position == ScrollbarPosition.LEFT:
            scrollable_layout = LayoutInfo(left=self.scrollbar_thickness, right=0, top=0, bottom=0)
            scrollbar_layout = LayoutInfo(left=0, top=0, bottom=0, width=self.scrollbar_thickness)
            orientation = Orientation.VERTICAL
        elif self.scrollbar_position == ScrollbarPosition.RIGHT:
            scrollable_layout = LayoutInfo(left=0, right=self.scrollbar_thickness, top=0, bottom=0)
            scrollbar_layout = LayoutInfo(right=0, top=0, bottom=0, width=self.scrollbar_thickness)
            orientation = Orientation.VERTICAL
        elif self.scrollbar_position == ScrollbarPosition.TOP:
            scrollable_layout = LayoutInfo(left=0, right=0, top=self.scrollbar_thickness, bottom=0)
            scrollbar_layout = LayoutInfo(left=0, right=0, top=0, height=self.scrollbar_thickness)
            orientation = Orientation.HORIZONTAL
        else:
            scrollable_layout = LayoutInfo(left=0, right=0, top=0, bottom=self.scrollbar_thickness)
            scrollbar_layout = LayoutInfo(left=0, right=0, bottom=0, height=self.scrollbar_thickness)
            orientation = Orientation.HORIZONTAL

        if self.scrollable is None:
            self.scrollable = self.scrollable_class(layout_info=scrollable_layout, container=self)
        else:
            self.scrollable.layout_info = scrollable_layout

        if self.scrollbar is None:
            self.scrollbar = Scrollbar(scrollbar_layout, self, orientation)
        else:
            self.scrollbar.layout_info = scrollbar_layout

        self.scrollbar.visible = self.scrollbar.thumb.ratio < 1.0

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)
        self._configure()
        super().layout(only_if_changed)
