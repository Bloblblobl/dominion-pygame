from enum import Enum

import pygame_gui

from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.components.default import layout0
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


class Scrollbar(UIElement):
    def __init__(self,
                 layout_info: LayoutInfo,
                 container: UIElement,
                 orientation: Orientation,
                 thumb_ratio: float):
        super().__init__(layout_info, container)
        self.orientation = orientation
        self.thumb_ratio = thumb_ratio
        self.offset = 0
        self.element = Panel(layout0, self, RED)
        self._configure_scrollbar()

    def _configure_scrollbar(self):
        if self.orientation == Orientation.HORIZONTAL:
            thumb_width = self.thumb_ratio * self.width
            thumb_layout = LayoutInfo(left=self.offset, top=0, bottom=0, width=thumb_width)
        else:
            thumb_height = self.thumb_ratio * self.height
            thumb_layout = LayoutInfo(left=0, right=0, top=self.offset, height=thumb_height)
        self.element.layout_info = thumb_layout

    def rebuild(self):
        self._configure_scrollbar()
        self.element.rebuild()


class ScrollContainer(UIElement, BaseEventHandler):
    def __init__(self,
                 layout_info: LayoutInfo,
                 container: UIElement,
                 scrollable_class,
                 scrollable_kwargs,
                 scrollbar_position: ScrollbarPosition,
                 scrollbar_thickness: int,
                 padding: LayoutInfo = None):
        super().__init__(layout_info, container, padding)
        self.scrollbar_position = scrollbar_position
        self.scrollbar_thickness = scrollbar_thickness

        self.scrollable = scrollable_class(container=self, **scrollable_kwargs)
        self.scrollable.container = self
        self.scrollbar = None
        self._configure()

        get_event_manager().subscribe(self.scrollbar, pygame_gui.UI_HORIZONTAL_SLIDER_MOVED, self.scrollable)

    def _configure(self):
        if self.scrollbar_position == ScrollbarPosition.LEFT:
            scrollable_layout = LayoutInfo(left=self.scrollbar_thickness, right=0, top=0, bottom=0)
            scrollbar_layout = LayoutInfo(left=0, top=0, bottom=0, width=self.scrollbar_thickness)
            scrollbar_orientation = Orientation.VERTICAL
        elif self.scrollbar_position == ScrollbarPosition.RIGHT:
            scrollable_layout = LayoutInfo(left=0, right=self.scrollbar_thickness, top=0, bottom=0)
            scrollbar_layout = LayoutInfo(right=0, top=0, bottom=0, width=self.scrollbar_thickness)
            scrollbar_orientation = Orientation.VERTICAL
        elif self.scrollbar_position == ScrollbarPosition.TOP:
            scrollable_layout = LayoutInfo(left=0, right=0, top=self.scrollbar_thickness, bottom=0)
            scrollbar_layout = LayoutInfo(left=0, right=0, top=0, height=self.scrollbar_thickness)
            scrollbar_orientation = Orientation.HORIZONTAL
        else:
            scrollable_layout = LayoutInfo(left=0, right=0, top=0, bottom=self.scrollbar_thickness)
            scrollbar_layout = LayoutInfo(left=0, right=0, bottom=0, height=self.scrollbar_thickness)
            scrollbar_orientation = Orientation.HORIZONTAL

        self.scrollable.layout_info = scrollable_layout

        width, height = self.scrollable.size
        content_width, content_height = self.scrollable.content_size

        thumb_ratio = width / content_width if scrollbar_orientation == Orientation.HORIZONTAL else height / content_height

        self.scrollbar = Scrollbar(scrollbar_layout, self, scrollbar_orientation, 0.5)
        self.layout(only_if_changed=False)

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)

    def rebuild(self):
        self._configure()
