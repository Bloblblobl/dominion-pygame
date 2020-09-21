import pygame
from typing import List, Union

from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.components.default import get_default_layout
from dominion_gui.components.pile import Pile
from dominion_gui.constants import card_spacing
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo

piles_per_row = 9


class Shop(UIElement, BaseEventHandler):
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, UIElement, None] = None,
                 padding: Union[LayoutInfo, None] = None):
        self._piles = []
        super().__init__(layout_info, container, padding)

    @property
    def piles(self):
        return self._piles

    @piles.setter
    def piles(self, pile_names: List[str]):
        self._piles = []
        for pile_name in pile_names:
            pile = Pile(layout_info=get_default_layout(),
                        container=self,
                        image_name=pile_name)

            self._piles.append(pile)

        self.layout(only_if_changed=False)

    def _calc_pile_size(self):
        pile_width = (self.width - (piles_per_row + 1) * card_spacing) / piles_per_row
        image_width, image_height = self.piles[0].image.dimensions
        aspect_ratio = image_height / image_width
        pile_height = int(pile_width * aspect_ratio)
        pile_width = int(pile_width)

        total_height = pile_height * 2 + card_spacing * 3
        if total_height <= self.height:
            return pile_width, pile_height

        pile_height = (self.height - 3 * card_spacing) / 2
        aspect_ratio = image_width / image_height
        pile_width = int(pile_height * aspect_ratio)
        pile_height = int(pile_height)
        return pile_width, pile_height

    def layout(self, only_if_changed=True):
        if self.container is not None:
            new_bounds = self.padded_rect
            if only_if_changed and new_bounds == self.bounds:
                return
            self._bounds = new_bounds

        if self.piles:
            pile_layouts = []
            pile_width, pile_height = self._calc_pile_size()
            initial_offset = (self.width - (piles_per_row - 1) * card_spacing - piles_per_row * pile_width) // 2
            left_offset = initial_offset
            top_offset = card_spacing

            for i, pile in enumerate(self.piles):
                if i != 0 and i % piles_per_row == 0:
                    left_offset = initial_offset
                    top_offset += pile_height + card_spacing

                new_layout = LayoutInfo(left=left_offset,
                                        top=top_offset,
                                        width=pile_width,
                                        height=pile_height)
                pile.layout_info = new_layout
                pile_layouts.append(new_layout)
                left_offset += pile_width + card_spacing

        for child in self.children:
            child.layout(only_if_changed)