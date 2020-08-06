from typing import Union

import pygame

from dominion_gui.components.default import layout0
from dominion_gui.constants import RED
from dominion_gui.ui_elements.html_textbox import HTMLTextBox
from dominion_gui.ui_elements.label import Label
from dominion_gui.ui_elements.panel import Panel
from dominion_gui.ui_elements.image import Image
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


counter_layout = LayoutInfo(right=5, bottom=5, width=30, height=30)
label_padding = LayoutInfo(left=4, right=4, top=4, bottom=4)


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

        html = f'<font face=fira_code size=2>{count}</font>'

        counter = HTMLTextBox(html,
                              counter_layout,
                              self.image,
                              bg_color=RED,
                              corner_radius=3,
                              wrap_to_height=True)
        return counter
