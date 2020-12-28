import pygame
from typing import Union, List

from dominion_gui.components.card import Card
from dominion_gui.components.card_view import CardView
from dominion_gui.components.default import get_default_layout
from dominion_gui.components.stack import Stack
from dominion_gui.constants import BLUE, RED
from dominion_gui.event_handler import EventHandler
from dominion_gui.ui_elements.button import Button
from dominion_gui.ui_elements.enums import Orientation, Position
from dominion_gui.ui_elements.horizontal_scroll_container import HorizontalScrollContainer
from dominion_gui.ui_elements.label import Label
from dominion_gui.ui_elements.ui_element import UIElement
from dominion_gui.ui_util import calculate_text_size
from layout_info.layout_info import LayoutInfo

button_padding = 10
stack_spacing = 5


class Response(UIElement, EventHandler):
    def __init__(self,
                 prompt_text: str,
                 card_names: List[str],
                 button_names: List[str],
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, 'UIElement', None] = None,
                 padding: Union[LayoutInfo, None] = None):
        super().__init__(layout_info, container, padding)
        self._subscribed_cards = []
        self.selected_cards = []

        label = Label(prompt_text, get_default_layout(), None)
        label_width, label_height = label.element.font.size(label.text)
        label.layout_info.width = label_width
        prompt_layout = LayoutInfo(left=0, right=0, top=0, height=label_height)
        prompt = Stack([label], 0, Orientation.HORIZONTAL, Position.CENTER, prompt_layout, self)

        card_view_li = LayoutInfo(left=0, right=0, top=0, height=.7)
        self.scroll_container = HorizontalScrollContainer(card_view_li, self, CardView, 0.035)
        self.card_view = self.scroll_container.scrollable
        self.card_view.on_scroll = self.get_on_scroll_override(old_on_scroll=self.card_view.on_scroll)
        self.card_view.cards = card_names
        self._subscribe_to_cards()

        self.buttons = {}
        button_stack = self.create_buttons(button_names)
        stack_elements = [prompt, self.card_view, button_stack]
        self.stack = Stack(ui_elements=stack_elements,
                           spacing=stack_spacing,
                           orientation=Orientation.VERTICAL,
                           alignment=Position.TOP,
                           layout_info=get_default_layout(),
                           container=self,
                           initial_spacing=True)

        self.layout(only_if_changed=False)

    def get_on_scroll_override(self, old_on_scroll):
        def on_scroll(direction):
            self._unsubscribe_from_cards()
            old_on_scroll(direction)
            self.layout(only_if_changed=False)
            self._subscribe_to_cards()
        return on_scroll

    def _unsubscribe_from_cards(self):
        for card in self._subscribed_cards:
            self.unsubscribe(card.image, 'on_click', self)
            self.unsubscribe(card.image, 'on_mouse_enter', self)
            self.unsubscribe(card.image, 'on_mouse_leave', self)
        self._subscribed_cards = []

    def _subscribe_to_cards(self):
        for card in self.card_view.cards:
            card.border_on_hover = False
            self.subscribe(card.image, 'on_click', self)
            self.subscribe(card.image, 'on_mouse_enter', self)
            self.subscribe(card.image, 'on_mouse_leave', self)
            self._subscribed_cards.append(card)

    def create_buttons(self, button_names):
        for name in button_names:
            button_width, button_height = calculate_text_size(name, button_padding)
            button_li = LayoutInfo(left=0, width=button_width, top=0, height=button_height)
            self.buttons[name] = Button(name, button_li, None)
        buttons = list(self.buttons.values())
        stack_height = buttons[0].height + stack_spacing
        return Stack(ui_elements=buttons,
                     spacing=stack_spacing,
                     orientation=Orientation.HORIZONTAL,
                     alignment=Position.CENTER,
                     layout_info=LayoutInfo(left=0, right=0, top=0, height=stack_height),
                     container=None)

    def on_click(self, *, ui_element):
        card = ui_element.container
        card_selected = card in self.selected_cards
        if card_selected:
            card.border.color = RED
            self.selected_cards.remove(card)
        else:
            card.border.color = BLUE
            self.selected_cards.append(card)
        self.on_card_select(card, card_selected)

    def on_mouse_enter(self, *, ui_element):
        card = ui_element.container
        card.border.visible = True

    def on_mouse_leave(self, *, ui_element):
        card = ui_element.container
        if card not in self.selected_cards:
            card.border.visible = False

    def on_card_select(self, card: Card, selected: bool):
        pass
