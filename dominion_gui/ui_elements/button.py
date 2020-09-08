from dataclasses import dataclass

import pygame
from pygame_gui.elements import UIButton

from dominion_gui.ui_elements.ui_element import UIElement


@dataclass
class BackgroundColors:
    Enabled: pygame.Color = None
    Disabled: pygame.Color = None


class Button(UIElement):
    def __init__(self,
                 text,
                 layout_info,
                 container,
                 bg_colors: BackgroundColors = None,
                 padding=None,
                 shape='rounded_rectangle',
                 corner_radius_ratio=None):
        self._corner_radius_ratio = corner_radius_ratio
        self.bg_colors = bg_colors

        super().__init__(layout_info, container, padding)
        self.element = UIButton(relative_rect=self.bounds,
                                manager=self.manager,
                                text=text)
        self.element.shape = shape
        self._set_colors(bg_colors)
        self.layout()

    def _set_colors(self, bg_colors):
        if bg_colors is None:
            return

        if bg_colors.Enabled is not None:
            self.element.colours['normal_bg'] = bg_colors.Enabled
        else:
            self.bg_colors.Enabled = self.element.colours['normal_bg']
        if bg_colors.Disabled is not None:
            self.element.colours['disabled_bg'] = bg_colors.Disabled
        else:
            self.bg_colors.Enabled = self.element.colours['disabled_bg']

    def on_enable(self, enabled: bool):
        super().on_enable(enabled)
        if self.bg_colors is None or self.element is None:
            return

        c = self.bg_colors
        self.element.colours['normal_bg'] = c.Enabled if enabled else c.Disabled
        self.rebuild()

    def layout(self, only_if_changed=True):
        super().layout(only_if_changed)

        if self.element is not None and self._corner_radius_ratio is not None:
            min_dimension = min(self.width, self.height)
            corner_radius = int(self._corner_radius_ratio * min_dimension)
            self.element.shape_corner_radius = corner_radius
            self.rebuild()
