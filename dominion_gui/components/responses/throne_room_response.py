import pygame
from typing import Union, List

from dominion_gui.components.card import Card
from dominion_gui.components.responses.response import Response
from dominion_gui.event_manager import ResponseEvent
from layout_info.layout_info import LayoutInfo

prompt_text = 'Select an Action card to play twice'
button_names = ['Done']


class ThroneRoomResponse(Response):
    def __init__(self,
                 card_names: List[str],
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, None] = None,
                 padding: Union[LayoutInfo, None] = None):
        super().__init__(prompt_text,
                         card_names,
                         button_names,
                         layout_info,
                         container,
                         padding)

        self.buttons['Done'].enabled = False
        self.subscribe(self.buttons['Done'], 'on_ui_button_press', self)

    def on_card_select(self, card: Card, selected: bool):
        self.buttons['Done'].enabled = len(self.selected_cards) == 1

    def on_ui_button_press(self, *, ui_element):
        selected_card_name = self.selected_cards[0].name
        response_event = pygame.event.Event(
            pygame.USEREVENT,
            dict(user_type='custom_event', event=ResponseEvent('throneroom', selected_card_name))
        )
        pygame.event.post(response_event)