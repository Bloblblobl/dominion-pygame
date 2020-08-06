from pygame_gui.elements import UITextBox

from dominion_gui.ui_elements.color_element import ColorElement


class HTMLTextBox(ColorElement):
    def __init__(self, html, layout_info, container, bg_color=None, padding=None):
        super().__init__(layout_info, container, padding)
        self._html = html
        self._background_color = bg_color
        self._build_textbox()

    @property
    def html(self):
        return self._html

    @html.setter
    def html(self, html):
        if html == self._html:
            return

        self._html = html
        self._build_textbox()

    def _build_textbox(self):
        if self.element is not None:
            self.element.kill()
        self.element = UITextBox(relative_rect=self.bounds,
                                 manager=self.manager,
                                 html_text=self.html)
        self.background_color = self._background_color

    def rebuild(self):
        self._build_textbox()
