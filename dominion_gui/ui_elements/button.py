from pygame_gui.elements import UIButton

from dominion_gui.ui_elements.ui_element import UIElement


class Button(UIElement):
    def __init__(self,
                 text,
                 layout_info,
                 container,
                 padding=None,
                 shape='rounded_rectangle',
                 corner_radius_ratio=None):
        self._corner_radius_ratio = corner_radius_ratio

        super().__init__(layout_info, container, padding)
        self.element = UIButton(relative_rect=self.bounds,
                                manager=self.manager,
                                text=text)
        self.element.shape = shape
        self.layout()

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)

        if self.element is not None and self._corner_radius_ratio is not None:
            min_dimension = min(self.width, self.height)
            corner_radius = int(self._corner_radius_ratio * min_dimension)
            self.element.shape_corner_radius = corner_radius
            self.rebuild()
