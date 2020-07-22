from dataclasses import dataclass
from typing import Union, Tuple

LayoutItem = Union[int, float, None]


@dataclass
class LayoutInfo:
    left: LayoutItem = None
    right: LayoutItem = None
    top: LayoutItem = None
    bottom: LayoutItem = None
    width: LayoutItem = None
    height: LayoutItem = None

    @property
    def is_valid(self):
        x_dimension = [self.left, self.right, self.width]
        y_dimension = [self.top, self.bottom, self.height]

        return x_dimension.count(None) == 1 and y_dimension.count(None) == 1

    def _absolutize(self, item: LayoutItem, parent: int):
        if not isinstance(item, float):
            return item

        if item > 1.0:
            return (item - int(item)) * parent + int(item)

        return item * parent

    def get_absolute_rect(self, size: Tuple[int, int]):
        w, h = size
        _left = self._absolutize(self.left, w)
        _right = self._absolutize(self.right, w)
        _top = self._absolutize(self.top, h)
        _bottom = self._absolutize(self.bottom, h)
        _width = self._absolutize(self.width, w)
        _height = self._absolutize(self.height, h)

        if _width is None:
            left = _left
            width = w - _left - _right
        else:
            left = w - _width - _right if _left is None else _left
            width = _width

        if _height is None:
            top = _top
            height = h - _top - _bottom
        else:
            top = h - _height - _bottom if _top is None else _top
            height = _height

        return left, top, width, height