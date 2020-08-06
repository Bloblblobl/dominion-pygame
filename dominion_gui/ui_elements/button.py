from pygame_gui.elements import UIButton

from dominion_gui.ui_elements.color_element import ColorElement


class Button(ColorElement):
    def __init__(self, text, layout_info, container, bg_color=None, padding=None):
        super().__init__(layout_info, container, padding)
        self.element = UIButton(relative_rect=self.bounds,
                                manager=self.manager,
                                text=text)
        self.background_color = bg_color