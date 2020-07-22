from dataclasses import dataclass
from typing import Union


@dataclass
class LayoutInfo:
    left: Union[int, float, None] = None
    right: Union[int, float, None] = None
    top: Union[int, float, None] = None
    bottom: Union[int, float, None] = None
    width: Union[int, float, None] = None
    height: Union[int, float, None] = None

    @property
    def is_valid(self):
        x_dimension = [self.left, self.right, self.width]
        y_dimension = [self.top, self.bottom, self.height]

        return x_dimension.count(None) == 1 and y_dimension.count(None) == 1

    def get_absolute_rect(self, size):
        ww, hh = size
        l, r, t, b, = self.left, self.right, self.top, self.bottom
        w, h = self.width, self.height

        l = int(l * ww) if isinstance(l, float) else l
        r = int(r * ww) if isinstance(r, float) else r
        t = int(t * hh) if isinstance(t, float) else t
        b = int(b * hh) if isinstance(b, float) else b
        w = int(w * ww) if isinstance(w, float) else w
        h = int(h * hh) if isinstance(h, float) else h

        if w is not None:
            left = l if l is not None else ww - w - r
            width = w
        else:
            left = l
            width = ww - l - r

        if h is not None:
            top = t if t is not None else hh - h - b
            height = h
        else:
            top = t
            height = hh - t - b

        return left, top, width, height