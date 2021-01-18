import pygame
from typing import Union, List

from dominion_gui.components.responses.response import Response
from dominion_gui.event_manager import ResponseEvent
from layout_info.layout_info import LayoutInfo

first_prompt_text = 'Select cards to trash'
second_prompt_text = 'Select cards to discard'
button_names = ['Done']


class SentryResponse(Response):
    def __init__(self,
                 card_names: List[str],
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, None] = None,
                 padding: Union[LayoutInfo, None] = None):
        super().__init__(first_prompt_text,
                         card_names,
                         button_names,
                         layout_info,
                         container,
                         padding)
        self.cards_to_trash = []
        self.cards_to_discard = []
        self.last_step = False

        self.subscribe(self.buttons['Done'], 'on_ui_button_press', self)

    def on_ui_button_press(self, *, ui_element):
        selected_card_names = [card.name for card in self.selected_cards]

        if self.last_step:
            self.cards_to_discard = selected_card_names
        else:
            self.cards_to_trash = selected_card_names

            if len(selected_card_names) != 2:
                next_cards = [card.name for card in self.card_view.cards if card not in self.selected_cards]
                self.selected_cards = []
                self.set_prompt_text(second_prompt_text)
                self.set_cards(next_cards)
                self.last_step = True
                return

        response_content = (self.cards_to_trash, self.cards_to_discard)
        response_event = pygame.event.Event(
            pygame.USEREVENT,
            dict(user_type='custom_event', event=ResponseEvent('sentry', response_content))
        )
        pygame.event.post(response_event)