from typing import Union
import pygame

from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


class ColorElement(UIElement):
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, UIElement, None] = None,
                 padding: Union[LayoutInfo, None] = None):
        super().__init__(layout_info, container, padding)

    @property
    def background_color(self):
        e = self.element
        if hasattr(e, 'background_colour'):
            return e.background_colour
        return e.bg_colour

    @background_color.setter
    def background_color(self, color):
        if color is None:
            return

        e = self.element
        if hasattr(e, 'background_colour'):
            e.background_colour = color
        else:
            e.bg_colour = color
        e.rebuild()
