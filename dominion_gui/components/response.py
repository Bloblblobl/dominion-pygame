import pygame
from typing import Union, List

from dominion_gui.components.card import Card
from dominion_gui.components.default import get_default_layout
from dominion_gui.ui_elements.label import Label
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


class Response(UIElement):
    def __init__(self,
                 prompt_text: str,
                 cards: List[Card] = [],
                 button_names: List[str] = [],
                 selected_card_count: int = 0,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, 'UIElement', None] = None,
                 padding: Union[LayoutInfo, None] = None):
        super().__init__(layout_info, container, padding)

        self.prompt = Label(prompt_text, get_default_layout(), self)

        self.layout(only_if_changed=False)

    def on_visible(self, visible: bool):
        super().on_visible(visible)

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)

        if hasattr(self, 'prompt'):
            text_width, text_height = self.prompt.element.font.size(self.prompt.text)
            self.prompt.layout_info.left = (self.width - text_width) // 2
            self.prompt.layout_info.width = text_width
            self.prompt.layout_info.height = text_height
            self.prompt.right = None
            self.prompt.bottom = None

            self.prompt.layout()

