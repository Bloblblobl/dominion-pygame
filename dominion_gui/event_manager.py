from collections import defaultdict

import pygame
import pygame_gui

from functools import partial
from dominion_gui.base_event_handler import BaseEventHandler

event_manager = None


def get_event_manager(root_element=None):
    return _get_event_manager(root_element)


def _get_event_manager(root_element):
    return __get_event_manager(root_element)


def __get_event_manager(root_element):
    global event_manager
    global _get_event_manager
    event_manager = EventManager(root_element)
    _get_event_manager = lambda x: event_manager
    return event_manager


def get_handler(subscriber: BaseEventHandler, event: pygame.event.Event):
    owner = event.ui_element.owner
    handler = None
    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
        handler = partial(subscriber.on_ui_button_pressed, owner)
    return handler


class EventManager:
    mouse_events = (pygame.MOUSEMOTION,
                    pygame.MOUSEBUTTONDOWN,
                    pygame.MOUSEBUTTONUP)
    events = (pygame.USEREVENT,) + mouse_events

    def __init__(self, root_element):
        self.subscribers = defaultdict(list)
        self.root_element = root_element

    def find_source_element(self, position, element=None):
        if element is None:
            element = self.root_element

        for child in element.children:
            if child.bounds.collidepoint(position):
                return self.find_source_element(position, child)
        return element

    def handle_event(self, event):
        if event.type == pygame.USEREVENT:
            if not hasattr(event.ui_element, 'owner'):
                return
            owner = event.ui_element.owner
            ui_event_type = event.user_type
        elif event.type in self.mouse_events:
            owner = self.find_source_element(event.pos)
            ui_event_type = event.type
        else:
            return

        for subscriber in self.subscribers[(id(owner), ui_event_type)]:
            get_handler(subscriber, event)()

    def subscribe(self,
                  owner,
                  event_type: pygame.event.Event,
                  subscriber: BaseEventHandler):
        self.subscribers[(id(owner), event_type)].append(subscriber)
