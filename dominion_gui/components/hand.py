from typing import Union
import pygame
from dominion_gui.game_client import GameClient
from dominion_gui.components.card_view import CardView
from dominion_gui.ui_elements.ui_element import UIElement
from dominion_gui.ui_player import your_turn_message
from layout_info.layout_info import LayoutInfo


your_turn = False


class Hand(CardView):
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, UIElement, None] = None,
                 padding: Union[LayoutInfo, None] = None
                 ):
        super().__init__(layout_info, container, padding)
        self.messages = []
        self.players = {}
        self.subscribe(owner=None,
                       handler_name='on_custom_event',
                       subscriber=self)
        self.your_turn = False

    def on_click(self, ui_element):
        card = ui_element.container
        GameClient.instance.play_action_card(card.name)

    def on_custom_event(self, event):
        global your_turn
        if event == 'done':
            your_turn = False
            for c in self.cards:
                c.enabled = False
        elif event == your_turn_message:
            your_turn = True
            for c in self.cards:
                c.enabled = True


