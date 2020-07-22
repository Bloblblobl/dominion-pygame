from pygame_gui.elements import ui_panel as pg_panel

from dominion_gui.components.ui_element import UIElement


class UIPanel(UIElement):
    def __init__(self, layout_info, container, bg_color):
        self._bounds = layout_info.get_absolute_rect(container)
        super().__init__(self.bounds, layout_info, container)
        self._panel = pg_panel.UIPanel(self.bounds, 0, self.manager)
        self.background_color = bg_color

    @property
    def background_color(self):
        return self._panel.background_colour

    @background_color.setter
    def background_color(self, color):
        self._panel.background_colour = color
        self._panel.rebuild()

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)
        if hasattr(self, '_panel'):
            self._panel.set_position(self.topleft)
            self._panel.set_dimensions(self.size)
            self._panel.rebuild()
