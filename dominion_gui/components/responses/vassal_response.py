import pygame
from typing import Union, List

from dominion_gui.components.responses.response import Response
from dominion_gui.event_manager import ResponseEvent
from layout_info.layout_info import LayoutInfo

prompt_text = 'Play this action card?'
button_names = ['Yes', 'No']


class VassalResponse(Response):
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

        self.subscribe(self.buttons['Yes'], 'on_ui_button_press', self)
        self.subscribe(self.buttons['No'], 'on_ui_button_press', self)

    def on_ui_button_press(self, *, ui_element):
        play_card = ui_element == self.buttons['Yes']
        response_event = pygame.event.Event(
            pygame.USEREVENT,
            dict(user_type='custom_event', event=ResponseEvent('vassal', play_card))
        )
        pygame.event.post(response_event)
