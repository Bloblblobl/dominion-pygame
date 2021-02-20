from typing import Union

import pygame

from dominion_gui.components.default import get_default_layout
from dominion_gui.constants import images_dir
from dominion_gui.event_handler import EventHandler
from dominion_gui.event_manager import CardZoomEvent, get_event_manager
from dominion_gui.ui_elements.image import Image
from dominion_gui.ui_elements.ui_element import UIElement
from dominion_gui.util import get_card_name
from layout_info.layout_info import LayoutInfo


class CardZoom(UIElement, EventHandler):
    def __init__(self,
                 layout_info: Union[LayoutInfo, None] = None,
                 container: Union[pygame.Rect, 'UIElement', None] = None,
                 padding: Union[LayoutInfo, None] = None):
        self.image = None
        super().__init__(layout_info=layout_info,
                         container=container,
                         padding=padding)
        get_event_manager().subscribe(None, 'on_custom_event', self)

    def set_image(self, image_name):
        if self.image is not None:
            self.image.kill()
            self.image = None

        if image_name is not None:
            image_path = f'{images_dir}/{get_card_name(image_name)}.jpg'
            self.image = Image(get_default_layout(), self, image_path)

    def on_custom_event(self, event):
        if isinstance(event, CardZoomEvent):
            self.set_image(event.card_name)
