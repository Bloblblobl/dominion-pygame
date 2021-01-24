import pygame
from typing import Union, List

from dominion_gui.components.card import Card
from dominion_gui.components.responses.response import Response
from dominion_gui.event_manager import ResponseEvent
from layout_info.layout_info import LayoutInfo

first_prompt_text = 'Select a card costing up to $5 to gain to your hand'
second_prompt_text = 'Select a card from your hand to put on top of your deck'
button_names = ['Done']


class ArtisanResponse(Response):
    def __init__(self,
                 supply_card_names: List[str],
                 hand_card_names: List[str],
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, None] = None,
                 padding: Union[LayoutInfo, None] = None):
        super().__init__(first_prompt_text,
                         supply_card_names,
                         button_names,
                         layout_info,
                         container,
                         padding)
        self.gain_card = None
        self.hand_card_names = hand_card_names

        self.buttons['Done'].enabled = False
        self.subscribe(self.buttons['Done'], 'on_ui_button_press', self)

    def on_card_select(self, card: Card, selected: bool):
        self.buttons['Done'].enabled = len(self.selected_cards) == 1

    def on_ui_button_press(self, *, ui_element):
        selected_card_name = [card.name for card in self.selected_cards][0]

        if self.gain_card is None:
            self.gain_card = selected_card_name
            self.set_prompt_text(second_prompt_text)
            self.selected_cards = []
            self.buttons['Done'].enabled = False
            self.set_cards(self.hand_card_names + [selected_card_name])
            return

        response_content = (self.gain_card, selected_card_name)
        response_event = pygame.event.Event(
            pygame.USEREVENT,
            dict(user_type='custom_event', event=ResponseEvent('artisan', response_content))
        )
        pygame.event.post(response_event)