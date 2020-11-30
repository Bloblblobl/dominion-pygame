import pygame

from dominion_gui.constants import RED
from dominion_gui.ui_elements.base_panel import BasePanel
from dominion_gui.ui_elements.ui_element import UIElement
from dominion_gui.util import Noneable
from layout_info.layout_info import LayoutInfo


class Border:
    def __init__(self,
                 thickness: int = 0,
                 color: pygame.color = RED,
                 visible: bool = False):
        self._thickness = thickness
        self._color = color
        self._visible = visible
        self.callback = None

    @property
    def thickness(self) -> int:
        return self._thickness

    @thickness.setter
    def thickness(self, t: int):
        self._thickness = t
        self.callback()

    @property
    def color(self) -> pygame.color:
        return self._color

    @color.setter
    def color(self, c: pygame.color):
        self._color = c
        self.callback()

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, v: bool):
        self._visible = v
        self.callback()


class Panel(BasePanel):
    def __init__(self,
                 layout_info: LayoutInfo,
                 container: UIElement,
                 background_color: Noneable(pygame.Color) = None,
                 padding: LayoutInfo = None,
                 depth: int = 0,
                 corner_radius: Noneable(int) = None,
                 border: Noneable(Border) = None):
        self.border = border
        self.border_panel = None
        super().__init__(layout_info, container, background_color, padding, depth, corner_radius)

        self.update_border()

    def update_border(self):
        if self.border is None:
            return

        if self.border.callback is None:
            self.border.callback = self.update_border

        bt = -self.border.thickness
        border_li = LayoutInfo(left=bt, right=bt, top=bt, bottom=bt)
        if self.border_panel is None:
            self.border_panel = BasePanel(border_li, self, self.border.color)
        else:
            self.border_panel.layout_info = border_li
            self.border_panel.background_color = self.border.color
        self.border_panel.visible = self.border.visible

    def add_child(self, child: 'UIElement'):
        if self.border_panel in self.children:
            self.children.remove(self.border_panel)
        super().add_child(child)
        if self.border_panel is not None:
            self.children.append(self.border_panel)

    def on_visible(self, visible: bool):
        super().on_visible(visible)
        self.update_border()

        # always hide the border if the panel itself is not visible
        if not visible:
            self.border_panel.visible = False

    def kill(self):
        super().kill()
        if self.border_panel is not None:
            self.border_panel.kill()
