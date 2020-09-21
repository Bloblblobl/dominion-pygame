import pygame_gui
from typing import Callable, Union

from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.constants import GRAY
from dominion_gui.event_manager import get_event_manager
from dominion_gui.ui_elements.button import Button, BackgroundColors
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


class HorizontalScrollContainer(UIElement, BaseEventHandler):
    def __init__(self,
                 layout_info: LayoutInfo,
                 container: UIElement,
                 scrollable_class: Callable,
                 button_thickness: Union[int, float],
                 padding: LayoutInfo = None):
        self.scrollable = None
        super().__init__(layout_info, container, padding)
        bg_colors = BackgroundColors(Disabled=GRAY)
        left_layout_info = LayoutInfo(left=0, top=0, bottom=0, width=button_thickness)
        right_layout_info = LayoutInfo(right=0, top=0, bottom=0, width=button_thickness)
        scrollable_layout = LayoutInfo(left=button_thickness, right=button_thickness, top=0, bottom=0)
        self.left_button = Button('<', left_layout_info, self, bg_colors)
        self.right_button = Button('>', right_layout_info, self, bg_colors)
        self.scrollable = scrollable_class(scrollable_layout, self)

        self.subscribe(self.left_button, pygame_gui.UI_BUTTON_PRESSED, self)
        self.subscribe(self.right_button, pygame_gui.UI_BUTTON_PRESSED, self)

    def on_ui_button_pressed(self, ui_element):
        direction = ''
        if ui_element == self.left_button:
            direction = 'left'
        elif ui_element == self.right_button:
            direction = 'right'

        self.scrollable.on_scroll(direction=direction)
        self.layout(only_if_changed=False)

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)

        if self.scrollable is not None:
            first_offset, last_offset = self.scrollable.visible_content
            self.left_button.visible = first_offset > 0
            self.right_button.visible = last_offset < 1
