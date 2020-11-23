import pygame
from typing import Union, List

from dominion_gui.components.card_view import CardView
from dominion_gui.components.default import get_default_layout
from dominion_gui.components.stack import Stack
from dominion_gui.ui_elements.button import Button
from dominion_gui.ui_elements.enums import Orientation, Position
from dominion_gui.ui_elements.label import Label
from dominion_gui.ui_elements.ui_element import UIElement
from dominion_gui.util import calculate_text_size
from layout_info.layout_info import LayoutInfo

button_padding = 10
stack_spacing = 5


class Response(UIElement):
    def __init__(self,
                 prompt_text: str,
                 card_names: List[str],
                 button_names: List[str],
                 selected_card_count: int = 0,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, 'UIElement', None] = None,
                 padding: Union[LayoutInfo, None] = None):
        super().__init__(layout_info, container, padding)

        label = Label(prompt_text, get_default_layout(), None)
        label_width, label_height = label.element.font.size(label.text)
        label.layout_info.width = label_width
        prompt_layout = LayoutInfo(left=0, right=0, top=0, height=label_height)
        prompt = Stack([label], 0, Orientation.HORIZONTAL, Position.CENTER, prompt_layout, self)
        self.card_view = CardView(LayoutInfo(left=0, right=0, top=0, height=.7), self)
        self.card_view.cards = card_names
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
