import pygame
from typing import Union, List, Callable

from dominion_gui.ui_elements.enums import Position, Orientation
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


class Stack(UIElement):
    def __init__(self,
                 ui_elements: List[Union[Callable, UIElement]],
                 spacing: int,
                 orientation: Orientation = Orientation.HORIZONTAL,
                 alignment: Position = Position.LEFT,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, UIElement, None] = None,
                 padding: Union[LayoutInfo, None] = None,
                 initial_spacing: bool = False):
        self._ui_elements = []
        self.spacing = spacing
        self.orientation = orientation
        self.alignment = alignment
        # whether there is spacing before the first element
        self.initial_spacing = initial_spacing
        super().__init__(layout_info, container, padding)
        self.ui_elements = ui_elements

    @property
    def valid(self):
        o = self.orientation
        a = self.alignment
        valid_horizontal_alignments = {
            Position.LEFT,
            Position.CENTER,
            Position.RIGHT
        }
        valid_vertical_alignments = {
            Position.TOP,
            Position.CENTER,
            Position.BOTTOM
        }
        if o == Orientation.HORIZONTAL and a in valid_horizontal_alignments:
            return True
        if o == Orientation.VERTICAL and a in valid_vertical_alignments:
            return True
        return False

    @property
    def ui_elements(self):
        return self._ui_elements

    @property
    def initial_offset(self):
        return self.spacing if self.initial_spacing else 0

    @ui_elements.setter
    def ui_elements(self, elements: List[Union[Callable, UIElement]]):
        for element in self._ui_elements:
            element.kill()
        self._ui_elements = []
        self.children = []
        for element in elements:
            if hasattr(element, '__call__'):
                element = element()
            element.container = self
            self._ui_elements.append(element)
        self.layout(only_if_changed=False)

    def _horizontal_layout(self):
        def left_layout(left):
            for element in self.ui_elements:
                element.layout_info.left = left
                if element.layout_info.width is None:
                    element.layout_info.width = element.width
                element.layout_info.right = None
                element.layout()
                left += element.layout_info.width + self.spacing

        if self.alignment == Position.LEFT:
            left = self.initial_offset
            left_layout(left)
        elif self.alignment == Position.CENTER:
            total_width = sum(e.width for e in self.ui_elements)
            total_width += self.spacing * (len(self.ui_elements) - 1)
            left = (self.width - total_width) // 2
            left_layout(left)
        else:
            right = self.initial_offset
            for element in self.ui_elements:
                element.layout_info.right = right
                if element.layout_info.width is None:
                    element.layout_info.width = element.width
                element.layout_info.left = None
                element.layout()
                right += element.layout_info.width + self.spacing

    def _vertical_layout(self):
        def top_layout(top):
            for element in self.ui_elements:
                element.layout_info.top = top
                if element.layout_info.height is None:
                    element.layout_info.height = element.height
                element.layout_info.bottom = None
                element.layout()
                top += element.layout_info.height + self.spacing

        if self.alignment == Position.TOP:
            top = self.initial_offset
            top_layout(top)
        elif self.alignment == Position.CENTER:
            total_height = sum(e.height for e in self.ui_elements)
            total_height += self.spacing * (len(self.ui_elements) - 1)
            top = (self.height - total_height) // 2
            top_layout(top)
        else:
            bottom = self.initial_offset
            for element in self.ui_elements:
                element.layout_info.bottom = bottom
                if element.layout_info.height is None:
                    element.layout_info.height = element.height
                element.layout_info.top = None
                element.layout()
                bottom += element.layout_info.height + self.spacing

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)
        if self.orientation == Orientation.HORIZONTAL:
            self._horizontal_layout()
        else:
            self._vertical_layout()
