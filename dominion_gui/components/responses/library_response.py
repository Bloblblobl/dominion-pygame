import pygame
from typing import Union, List

from dominion_gui.components.responses.response import Response
from dominion_gui.event_manager import ResponseEvent
from layout_info.layout_info import LayoutInfo

prompt_text = 'Select any action cards to set aside. You will be drawing {} cards'
button_names = ['Done']


class LibraryResponse(Response):
    def __init__(self,
                 candidate_card_names: List[str],
                 hand_count: int,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, None] = None,
                 padding: Union[LayoutInfo, None] = None):
        # library is still in hand at this point, so we subtract from 8 instead of 7
        self.expected_count = 8 - hand_count
        initial_count = min(self.expected_count, len(candidate_card_names))
        initial_candidates = candidate_card_names[:initial_count]
        super().__init__(prompt_text.format(self.expected_count),
                         initial_candidates,
                         button_names,
                         layout_info,
                         container,
                         padding)
        self.remaining_candidates = candidate_card_names[initial_count:]
        self.subscribe(self.buttons['Done'], 'on_ui_button_press', self)

    def on_ui_button_press(self, *, ui_element):
        next_cards = ([card.name for card in self.card_view.cards if card not in self.selected_cards])

        remaining_count = self.expected_count - len(next_cards)
        if len(self.remaining_candidates) >= remaining_count > 0:
            next_cards.extend(self.remaining_candidates[:remaining_count])
            self.remaining_candidates = self.remaining_candidates[remaining_count:]
            self.selected_cards = []
            self.set_cards(next_cards)
            return

        response_event = pygame.event.Event(
            pygame.USEREVENT,
            dict(user_type='custom_event', event=ResponseEvent('library', next_cards))
        )
        pygame.event.post(response_event)