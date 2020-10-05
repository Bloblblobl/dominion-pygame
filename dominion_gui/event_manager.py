from collections import defaultdict

import pygame
import pygame_gui

from functools import partial
from dominion_gui.base_event_handler import BaseEventHandler

event_manager = None

first_card = None


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

    if event.type == MouseEvent.Enter:
        handler = partial(subscriber.on_mouse_enter, owner)
    elif event.type == MouseEvent.Leave:
        handler = partial(subscriber.on_mouse_leave, owner)
    elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
        handler = partial(subscriber.on_ui_button_pressed, owner)
    return handler


class MouseEvent:
    Enter = 'mouse_enter'
    Leave = 'mouse_leave'

    def __init__(self, owner, mouse_event_type, mouse_position):
        self.ui_element = lambda: None
        self.ui_element.owner = owner
        self.type = mouse_event_type
        self.mouse_position = mouse_position


class EventManager:
    mouse_events = (pygame.MOUSEMOTION,
                    pygame.MOUSEBUTTONDOWN,
                    pygame.MOUSEBUTTONUP)
    events = (pygame.USEREVENT,) + mouse_events

    def __init__(self, root_element):
        self.subscribers = defaultdict(list)
        self.root_element = root_element
        self.current_element = None

    def find_source_element(self, position, element=None):
        if element is None:
            element = self.root_element

        for child in element.children:
            if child.mouse_target and child.bounds.collidepoint(position):
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

            if ui_event_type == pygame.MOUSEMOTION:
                if owner == self.current_element:
                    return

                print(owner)
                print(self.current_element)
                leave_event = MouseEvent(self.current_element, MouseEvent.Leave, event.pos)
                self.handle_event(leave_event)
                self.current_element = owner
                enter_event = MouseEvent(owner, MouseEvent.Enter, event.pos)
                self.handle_event(enter_event)
                return
        elif event.type in (MouseEvent.Enter, MouseEvent.Leave):
            owner = event.ui_element.owner
            ui_event_type = event.type
        else:
            return

        for subscriber in self.subscribers[(id(owner), ui_event_type)]:
            get_handler(subscriber, event)()

    def subscribe(self,
                  owner,
                  event_type,
                  subscriber: BaseEventHandler):
        self.subscribers[(id(owner), event_type)].append(subscriber)

    def unsubscribe(self, owner, event_type):
        del self.subscribers[(id(owner), event_type)]
