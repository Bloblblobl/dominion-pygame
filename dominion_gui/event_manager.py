from collections import defaultdict

import pygame
import pygame_gui

from functools import partial
from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.ui_elements.ui_element import UIElement


def get_handler(subscriber: BaseEventHandler, event: pygame.event.Event):
    owner = event.ui_element.owner
    handler = None
    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
        handler = partial(subscriber.on_ui_button_pressed, owner)
    return handler


class EventManager:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            owner = event.ui_element.owner
            ui_event_type = event.user_type
            for subscriber in self.subscribers[(id(owner), ui_event_type)]:
                get_handler(subscriber, event)()

    def subscribe(self,
                  owner: UIElement,
                  event_type: pygame.event.Event,
                  subscriber: BaseEventHandler):
        self.subscribers[(id(owner), event_type)].append(subscriber)


event_manager = EventManager()
