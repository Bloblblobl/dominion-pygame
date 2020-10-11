from collections import defaultdict
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


def delegate(f):
    def decorated(*args, **kwargs):
        handler_name = f.__name__

        # args[0] is the event manager
        subscribers = args[0].subscribers
        # remove args[0] (self) because the handler is a bound method
        args = args[1:]
        owner = kwargs.get('ui_element', None)
        for subscriber in subscribers[(id(owner), handler_name)]:
            handler = getattr(subscriber, handler_name)
            handler(*args, **kwargs)
    return decorated


class EventManager(BaseEventHandler):
    def __init__(self, root_element):
        self.subscribers = defaultdict(list)
        self.root_element = root_element
        self.current_element = None

    def find_source_element(self, x, y, element=None):
        if element is None:
            element = self.root_element

        for child in element.children:
            if child.mouse_target and child.bounds.collidepoint((x, y)):
                return self.find_source_element(x, y, child)
        return element

    def subscribe(self,
                  owner,
                  handler_name: str,
                  subscriber: BaseEventHandler):
        self.subscribers[(id(owner), handler_name)].append(subscriber)

    def unsubscribe(self, owner, handler_name: str):
        del self.subscribers[(id(owner), handler_name)]

    def on_mouse_move(self, x, y):
        owner = self.find_source_element(x, y)
        if owner == self.current_element:
            return

        self.on_mouse_leave(ui_element=self.current_element)
        self.current_element = owner
        self.on_mouse_enter(ui_element=self.current_element)

    @delegate
    def on_mouse_button_down(self, button):
        pass

    @delegate
    def on_mouse_button_up(self, button):
        pass

    @delegate
    def on_mouse_scroll(self, direction):
        pass

    @delegate
    def on_key_down(self, key, modifiers):
        pass

    @delegate
    def on_key_up(self, key, modifiers):
        pass

    @delegate
    def on_mouse_enter(self, ui_element):
        pass

    @delegate
    def on_mouse_leave(self, ui_element):
        pass

    @delegate
    def on_ui_button_pressed(self, *, ui_element):
        pass

    @delegate
    def on_ui_button_hovered(self, *, ui_element):
        pass

    @delegate
    def on_ui_button_unhovered(self, *, ui_element):
        pass

    @delegate
    def on_ui_text_entry_changed(self, *, ui_element, text):
        pass

    @delegate
    def on_ui_text_entry_finished(self, *, ui_element, text):
        pass

    @delegate
    def on_ui_drop_down_menu_changed(self, *, ui_element, option):
        pass

    @delegate
    def on_ui_textbox_link_clicked(self, *, ui_element, link_target):
        pass

    @delegate
    def on_ui_horizontal_slider_moved(self, *, ui_element, slider_value):
        pass

    @delegate
    def on_ui_selection_list_new_selection(self, *, ui_element, selection):
        pass

    @delegate
    def on_ui_selection_list_dropped_selection(self, *, ui_element, selection):
        pass

    @delegate
    def on_ui_window_closed(self, *, ui_element):
        pass

    @delegate
    def on_ui_window_moved_to_front(self, *, ui_element):
        pass

    @delegate
    def on_ui_confirmation_dialog_confirmed(self, *, ui_element):
        pass

    @delegate
    def on_ui_file_dialog_path_picked(self, *, ui_element, filepath):
        pass
