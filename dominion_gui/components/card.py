from typing import Union

import pygame

from dominion_gui import util
from dominion_gui.components.default import get_default_layout
from dominion_gui.constants import DARK_GRAY, images_dir
from dominion_gui.ui_elements.html_textbox import HTMLTextBox
from dominion_gui.ui_elements.image import Image
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


counter_layout = LayoutInfo(right=2, bottom=2, width=32, height=34)


class Card(UIElement):
    def __init__(self,
                 image_name: str,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, 'UIElement', None] = None,
                 padding: Union[LayoutInfo, None] = None,
                 count: int = -1):
        self.name = util.get_card_class(image_name)
        self.image = None
        self.image_path = f'{images_dir}/{image_name}.jpg'
        self.gray_image_path = f'{images_dir}/{image_name}_gray.jpg'
        super().__init__(layout_info, container, padding)
        self.counter = self.build_counter(count)

    def on_enable(self, enabled: bool):
        image_path = self.image_path if enabled else self.gray_image_path
        if self.image is not None:
            self.image.kill()
        self.image = Image(get_default_layout(), self, image_path)

    def build_counter(self, count):
        if count == -1:
            return

        html = f'<font face=fira_code size=3>{count}</font>'

        counter = HTMLTextBox(html,
                              counter_layout,
                              self.image,
                              bg_color=DARK_GRAY,
                              corner_radius=5,
                              wrap_to_height=True)
        return counter
