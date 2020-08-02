from pygame_gui.elements import UITextBox

from dominion_gui.ui_elements.ui_element import UIElement


class TextBox(UIElement):
    def __init__(self, text, layout_info, container, bg_color=None, padding=None):
        super().__init__(layout_info, container, padding)
        self.text = text
        self._background_color = bg_color
        self._build_textbox()

    @property
    def html_text(self):
        return self.text

    def _build_textbox(self):
        if self.element is not None:
            self.element.kill()
        self.element = UITextBox(self.html_text, self.bounds, self.manager)
        self.background_color = self._background_color

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)
        if self.element is not None:
            self._build_textbox()
