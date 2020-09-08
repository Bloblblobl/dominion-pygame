import copy

import pygame
from typing import List, Union

from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.components.card import Card
from dominion_gui.components.default import get_default_layout
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo

card_spacing = 5


class Hand(UIElement, BaseEventHandler):
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, UIElement, None] = None,
                 padding: Union[LayoutInfo, None] = None):
        self._cards = []
        self.first_index = 0
        self.last_index = 0
        super().__init__(layout_info, container, padding)

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, card_names: List[str]):
        self._cards = []
        for card_name in card_names:
            card = Card(layout_info=get_default_layout(),
                        container=self,
                        image_name=card_name)

            self._cards.append(card)

        self.layout(only_if_changed=False)

    @property
    def visible_content(self):
        if not self.cards:
            return (0, 0)
        return (self.first_index / (len(self.cards) - 1),
                self.last_index / (len(self.cards) - 1))

    def on_scroll(self, direction, delta=1):
        if direction == 'left':
            self.first_index = max(self.first_index - delta, 0)
        elif direction == 'right':
            self.first_index = min(self.first_index + delta, len(self.cards) - 1)

    def layout(self, only_if_changed=True):
        left_offset = 0
        overflow = False
        for i, card in enumerate(self.cards):
            if i < self.first_index or overflow:
                card.layout_info.width = 0
                continue
            image_width, image_height = card.image.dimensions
            _, hand_height = self.padded_rect.size
            aspect_ratio = image_width / image_height
            new_width = int(hand_height * aspect_ratio)
            if left_offset + new_width > self.padded_rect.width:
                self.last_index = i - 1
                card.layout_info.width = 0
                overflow = True
                continue
            new_layout = LayoutInfo(left=left_offset, top=0, bottom=0, width=new_width)
            card.layout_info = new_layout
            left_offset += new_width + card_spacing

        if not overflow:
            self.last_index = len(self.cards) - 1

        super().layout(only_if_changed)

    def on_ui_horizontal_slider_moved(self, ui_element, slider_value):
        print(slider_value)
