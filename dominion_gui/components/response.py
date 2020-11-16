import pygame
from typing import Union, List

from dominion_gui.components.card import Card
from dominion_gui.components.card_view import CardView
from dominion_gui.components.default import get_default_layout
from dominion_gui.ui_elements.label import Label
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


class Response(UIElement):
    def __init__(self,
                 prompt_text: str,
                 card_names: List[str],
                 button_names: List[str],
                 selected_card_count: int = 0,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, 'UIElement', None] = None,
                 padding: Union[LayoutInfo, None] = None):
        super().__init__(layout_info, container, padding)

        self.prompt = Label(prompt_text, get_default_layout(), self)
        self.card_view = CardView(get_default_layout(), self)
        self.card_view.cards = card_names

        self.layout(only_if_changed=False)

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)

        if hasattr(self, 'prompt'):
            text_width, text_height = self.prompt.element.font.size(self.prompt.text)
            self.prompt.layout_info.left = (self.width - text_width) // 2
            self.prompt.layout_info.width = text_width
            self.prompt.layout_info.height = text_height
            self.prompt.layout_info.right = None
            self.prompt.layout_info.bottom = None
            self.card_view.layout_info.top = text_height

            self.prompt.layout()
            self.card_view.layout()

