from pygame_gui.elements import UITextBox

from dominion_gui.ui_elements.color_element import ColorElement


class HTMLTextBox(ColorElement):
    def __init__(self,
                 html,
                 layout_info,
                 container,
                 bg_color=None,
                 padding=None,
                 corner_radius=None,
                 wrap_to_height=False):
        super().__init__(layout_info, container, padding)
        self._html = html
        self._background_color = bg_color
        self._shape = None
        self._shape_corner_radius = None
        self._wrap_to_height = wrap_to_height
        self._build_textbox()

        if corner_radius is not None:
            self._shape = 'rounded_rectangle'
            self._shape_corner_radius = corner_radius
            self.rebuild()

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
        new_element = UITextBox(relative_rect=self.bounds,
                                manager=self.manager,
                                html_text=self.html,
                                wrap_to_height=self._wrap_to_height)

        if self._shape is not None:
            new_element.shape = self._shape
        if self._shape_corner_radius is not None:
            new_element.shape_corner_radius = self._shape_corner_radius

        if self.element is not None:
            self.kill()
        self.element = new_element
        self.background_color = self._background_color
        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        sb = self.element.scroll_bar
        if sb is not None:
            sb.start_percentage = 1.0 - sb.sliding_button.rect.height / sb.scrollable_height
            sb.has_moved_recently = True
            new_y = sb.scrollable_height - sb.sliding_button.rect.height + sb.arrow_button_height
            new_pos = (sb.sliding_rect_position.x, new_y)
            sb.sliding_button.set_relative_position(new_pos)

    def rebuild(self):
        self._build_textbox()
        self.element.rebuild()