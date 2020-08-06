from pygame_gui.elements import UIPanel

from dominion_gui.ui_elements.color_element import ColorElement


class Panel(ColorElement):
    def __init__(self, layout_info, container, bg_color=None, padding=None):
        super().__init__(layout_info, container, padding)
        self.element = UIPanel(relative_rect=self.bounds,
                               manager=self.manager,
                               starting_layer_height=0)
        self.background_color = bg_color
