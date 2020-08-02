from pygame_gui.elements import UIImage

from dominion_gui.ui_elements.ui_element import UIElement


class Image(UIElement):
    def __init__(self, layout_info, container, bg_color=None, padding=None):
        super().__init__(layout_info, container, padding)
        self.element = UIImage(self.bounds, 0, self.manager)
        self.background_color = bg_color
