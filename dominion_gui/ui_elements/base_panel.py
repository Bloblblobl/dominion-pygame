from pygame_gui.elements import UIPanel

from dominion_gui.ui_elements.color_element import ColorElement


class BasePanel(ColorElement):
    def __init__(self,
                 layout_info,
                 container,
                 background_color=None,
                 padding=None,
                 depth=0,
                 corner_radius=None):
        super().__init__(layout_info, container, padding)
        self.element = UIPanel(relative_rect=self.bounds,
                               manager=self.manager,
                               starting_layer_height=depth)
        self.background_color = background_color

        if corner_radius is not None:
            self.element.shape = 'rounded_rectangle'
            self.element.shape_corner_radius = corner_radius
            self.rebuild()
