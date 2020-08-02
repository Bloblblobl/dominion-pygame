from pygame_gui.elements import UIButton

from dominion_gui.ui_elements.ui_element import UIElement


class Button(UIElement):
    def __init__(self, button_text, layout_info, container, bg_color=None, padding=None):
        super().__init__(layout_info, container, padding)
        self.element = UIButton(self.bounds, button_text, self.manager)
        self.background_color = bg_color

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)
        if self.element is not None:
            self.element.set_position(self.topleft)
            self.element.set_dimensions(self.size)
            self.element.rebuild()