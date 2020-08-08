from typing import Union

import pygame

from dominion_gui.components.default import layout0
from dominion_gui.constants import DARK_GRAY
from dominion_gui.ui_elements.html_textbox import HTMLTextBox
from dominion_gui.ui_elements.image import Image
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


counter_layout = LayoutInfo(right=2, bottom=2, width=32, height=34)


class Card(UIElement):
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, 'UIElement', None] = None,
                 padding: Union[LayoutInfo, None] = None,
                 image_path='artisan.png',
                 count=None):
        super().__init__(layout_info, container, padding)
        self.image = Image(layout0, self, image_path)
        self.counter = self.build_counter(count)

    def build_counter(self, count):
        if count is None:
            return

        html = f'<font face=fira_code size=3>{count}</font>'

        counter = HTMLTextBox(html,
                              counter_layout,
                              self.image,
                              bg_color=DARK_GRAY,
                              corner_radius=5,
                              wrap_to_height=True)
        return counter
