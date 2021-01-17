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
        self.selected_cards = []

        self.label = Label(prompt_text, get_default_layout(), None)
        label_width, label_height = self.label.element.font.size(self.label.text)
        self.label.layout_info.width = label_width
        prompt_layout = LayoutInfo(left=0, right=0, top=0, height=label_height)
        prompt = Stack([self.label], 0, Orientation.HORIZONTAL, Position.CENTER, prompt_layout, self)

        self.card_view = CardView(LayoutInfo(left=0, right=0, top=0, height=.7), self)
        self.card_view.cards = card_names
        for card in self.card_view.cards:
            card.border_on_hover = False
            self.subscribe(card.image, 'on_click', self)
            self.subscribe(card.image, 'on_mouse_enter', self)
            self.subscribe(card.image, 'on_mouse_leave', self)

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

    def set_prompt_text(self, prompt_text):
        self.label.set_text(prompt_text)
        label_width, label_height = self.label.element.font.size(self.label.text)
        self.label.layout_info.width = label_width
        self.label.layout(only_if_changed=False)

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
