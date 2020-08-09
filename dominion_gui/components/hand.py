import pygame
from typing import List, Union

from dominion_gui.components.card import Card
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


class Hand(UIElement):
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, UIElement, None] = None,
                 padding: Union[LayoutInfo, None] = None,
                 card_padding: Union[LayoutInfo, None] = None):
        super().__init__(layout_info, container, padding)
        self.card_padding = card_padding
        self._cards = []

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, card_names: List[str]):
        self._cards = []
        for card_name in card_names:
            card_layout = LayoutInfo()
            card = Card(layout_info=card_layout,
                        container=self,
                        padding=self.card_padding,
                        image_name=card_name)
            self._cards.append(card)