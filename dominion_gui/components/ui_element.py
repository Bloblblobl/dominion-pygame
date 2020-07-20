from dataclasses import dataclass

from typing import Union
import pygame

from dominion_gui.components.ui_manager import get_manager


@dataclass
class AnchorInfo:
    left: Union[int, float]
    right: Union[int, float]
    top: Union[int, float]
    bottom: Union[int, float]


class UIElement(pygame.Rect):
    def __init__(self,
                 anchor_info: AnchorInfo,
                 container: Union[pygame.Rect, None]):
        self.anchor_info = anchor_info
        self.container = container
        self.children = []
        self.layout()
        super().__init__(self.topleft, self.size)

    # def __eq__(self, other: pygame.Rect):
    #     return self.topleft == other.topleft and self.size == other.size

    @property
    def manager(self):
        return get_manager()

    @property
    def topleft(self):
        return super().topleft

    @topleft.setter
    def topleft(self, tl):
        if tl == self.topleft:
            return
        pygame.Rect.topleft = tl
        self.layout(only_if_changed=False)

    @property
    def size(self):
        return super().size

    @size.setter
    def size(self, s):
        if s == self.size:
            return
        super().size = s
        self.layout(only_if_changed=False)

    @property
    def width(self):
        return super().width

    @width.setter
    def width(self, w):
        if w == self.width:
            return
        super().width = w
        self.layout(only_if_changed=False)

    @property
    def height(self):
        return super().height

    @height.setter
    def height(self, h):
        if h == self.height:
            return
        super().height = h
        self.layout(only_if_changed=False)

    def layout(self, only_if_changed=True):
        if self.container is not None:
            c = self.container
            ai = self.anchor_info
            left = ai.left if isinstance(ai.left, int) else ai.left * c.width
            right = ai.right if isinstance(ai.right, int) else ai.right * c.width
            top = ai.top if isinstance(ai.top, int) else ai.top * c.height
            bottom = ai.bottom if isinstance(ai.bottom, int) else ai.bottom * c.height
            width = c.width - (left + right)
            height = c.height - (top + bottom)
            new_bounds = pygame.Rect(left, top, width, height)
            if only_if_changed and new_bounds == self:
                return
            s = super()
            val = new_bounds.topleft
            s.topleft = val
            s.size = new_bounds.size
        for child in self.children:
            child.layout()
