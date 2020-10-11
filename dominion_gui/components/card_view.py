import pygame
from typing import List, Union

from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.components.card import Card
from dominion_gui.components.default import get_default_layout
from dominion_gui.constants import card_spacing
from dominion_gui.event_manager import get_event_manager
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


class CardView(UIElement, BaseEventHandler):
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, UIElement, None] = None,
                 padding: Union[LayoutInfo, None] = None):
        self._cards = []
        self.first_index = 0
        self.last_index = 0
        super().__init__(layout_info, container, padding)

    def _kill_cards(self):
        for card in self._cards:
            card.image.kill()
            if card.counter is not None:
                card.counter.kill()

    @property
    def cards(self):
        return self._cards

    @cards.setter
    def cards(self, card_names: List[str]):
        self._kill_cards()
        self._cards = []
        for card_name in card_names:
            card = Card(layout_info=get_default_layout(),
                        container=self,
                        image_name=card_name)

            get_event_manager().subscribe(card.image, 'on_mouse_enter', self)
            get_event_manager().subscribe(card.image, 'on_mouse_leave', self)

            self._cards.append(card)

        self.layout(only_if_changed=False)

    @property
    def visible_content(self):
        if not self.cards:
            return (0, 0)
        adjusted_len = len(self.cards) - 1 if len(self.cards) > 1 else 1
        return (self.first_index / adjusted_len,
                self.last_index / adjusted_len)

    def on_scroll(self, direction, delta=1):
        if direction == 'left':
            self.first_index = max(self.first_index - delta, 0)
        elif direction == 'right':
            self.first_index = min(self.first_index + delta, len(self.cards) - 1)

    def on_mouse_enter(self, ui_element):
        card = ui_element.card
        card.enabled = False

    def on_mouse_leave(self, ui_element):
        card = ui_element.card
        card.enabled = True

    def layout(self, only_if_changed=True):
        if self.container is not None:
            new_bounds = self.padded_rect
            if only_if_changed and new_bounds == self.bounds:
                return
            self._bounds = new_bounds

        left_offset = 0
        card_layouts = []
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
            card_layouts.append(new_layout)
            left_offset += new_width + card_spacing

        if not overflow:
            self.last_index = len(self.cards) - 1 if self.cards else 0

        left_offset -= card_spacing
        remaining_width = self.width - left_offset
        for layout in card_layouts:
            layout.left += remaining_width // 2

        for child in self.children:
            child.layout(only_if_changed)
