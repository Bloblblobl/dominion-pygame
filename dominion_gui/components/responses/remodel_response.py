import pygame
from typing import Union, List

from dominion_gui import util
from dominion_gui.components.card import Card
from dominion_gui.components.responses.response import Response
from dominion_gui.event_manager import ResponseEvent
from layout_info.layout_info import LayoutInfo

first_prompt_text = 'Select a card to trash from your hand'
second_prompt_text = 'Select a card to gain costing up to $2 more than '
button_names = ['Done']


class RemodelResponse(Response):
    def __init__(self,
                 supply_card_names: List[str],
                 hand_card_names: List[str],
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, None] = None,
                 padding: Union[LayoutInfo, None] = None):
        super().__init__(first_prompt_text,
                         hand_card_names,
                         button_names,
                         layout_info,
                         container,
                         padding)
        self.trash_card = None
        self.supply_card_names = supply_card_names

        self.buttons['Done'].enabled = False
        self.subscribe(self.buttons['Done'], 'on_ui_button_press', self)

    def on_card_select(self, card: Card, selected: bool):
        self.buttons['Done'].enabled = len(self.selected_cards) == 1

    def on_ui_button_press(self, *, ui_element):
        selected_card_name = [card.name for card in self.selected_cards][0]

        if self.trash_card is None:
            self.trash_card = selected_card_name
            self.set_prompt_text(second_prompt_text + selected_card_name)
            self.selected_cards = []
            self.buttons['Done'].enabled = False

            next_cards = self.supply_card_names
            trash_card_data = util.get_card_data(self.trash_card)
            if trash_card_data is not None:
                next_cards = util.filter_card_names(next_cards, f'card.cost <= {trash_card_data["Cost"] + 2}')
            self.set_cards(next_cards)
            return

        response_content = (self.trash_card, selected_card_name)
        response_event = pygame.event.Event(
            pygame.USEREVENT,
            dict(user_type='custom_event', event=ResponseEvent('remodel', response_content))
        )
        pygame.event.post(response_event)