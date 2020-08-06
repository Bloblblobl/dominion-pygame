from pygame_gui.elements import UIButton

from dominion_gui.ui_elements.ui_element import UIElement


class Button(UIElement):
    def __init__(self,
                 text,
                 layout_info,
                 container,
                 padding=None,
                 shape='rounded_rectangle',
                 corner_radius=None):
        super().__init__(layout_info, container, padding)
        self.element = UIButton(relative_rect=self.bounds,
                                manager=self.manager,
                                text=text)
        self.element.shape = shape
        min_dimension = min(self.width, self.height)
        corner_radius = int(0.2 * min_dimension) if corner_radius is None else corner_radius
        self.element.shape_corner_radius = corner_radius
        self.rebuild()
