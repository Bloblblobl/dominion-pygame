from pygame_gui.elements import UILabel

from dominion_gui.ui_elements.color_element import ColorElement


class Label(ColorElement):
    def __init__(self, text, layout_info, container, bg_color=None, padding=None):
        super().__init__(layout_info, container, padding)
        self.element = UILabel(relative_rect=self.bounds,
                               manager=self.manager,
                               text=text)
        self.background_color = bg_color