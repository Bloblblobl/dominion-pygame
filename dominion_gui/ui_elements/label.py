from pygame_gui.elements import UILabel

from dominion_gui.constants import TRANSPARENT, BLACK
from dominion_gui.ui_elements.color_element import ColorElement


class Label(ColorElement):
    def __init__(self,
                 text,
                 layout_info,
                 container,
                 text_color=BLACK,
                 background_color=TRANSPARENT,
                 padding=None):
        super().__init__(layout_info, container, padding)
        self.text = text
        self.element = UILabel(relative_rect=self.bounds,
                               manager=self.manager,
                               text=text)
        self.text_color = text_color
        self.background_color = background_color

    @property
    def text_color(self):
        return self.element.text_colour

    @text_color.setter
    def text_color(self, color):
        if color is None:
            return

        self.element.text_colour = color
        self.element.rebuild()
