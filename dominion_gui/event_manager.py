from enum import Enum

from dominion_gui.event_handler import EventHandler

event_manager = None

MouseButton = Enum('MouseButton', 'Left Middle Right')
Direction = Enum('Direction', 'Left Right Up Down')


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
    def decorated(event_manager, *args, **kwargs):
        handler_name = f.__name__

        subscribers = event_manager.subscribers
        owner = kwargs.get('ui_element', None)
        if (id(owner), handler_name) in subscribers:
            for subscriber in subscribers[(id(owner), handler_name)]:
                handler = getattr(subscriber, handler_name)
                handler(*args, **kwargs)

        f(event_manager, *args, **kwargs)
    return decorated


class EventManager(EventHandler):
    def __init__(self, root_element):
        self.subscribers = {}
        self.root_element = root_element
        self.current_element = None
        # element under the mouse cursor on mouse button down event
        self.pressed_element = None

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
                  subscriber: EventHandler):
        if not hasattr(self, handler_name):
            raise ValueError('No such handler ' + handler_name)
        self.subscribers.setdefault((id(owner), handler_name), []).append(subscriber)

    def unsubscribe(self, owner, handler_name: str):
        if (id(owner), handler_name) in self.subscribers:
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
        self.pressed_element = self.current_element

    @delegate
    def on_mouse_button_up(self, button):
        if self.current_element == self.pressed_element:
            self.on_click(ui_element=self.current_element)

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
    def on_mouse_enter(self, *, ui_element):
        pass

    @delegate
    def on_mouse_leave(self, *, ui_element):
        pass

    @delegate
    def on_click(self, *, ui_element):
        pass

    @delegate
    def on_custom_event(self, event):
        pass

    @delegate
    def on_ui_button_press(self, *, ui_element):
        pass

    @delegate
    def on_ui_text_entry_change(self, *, ui_element, text):
        pass

    @delegate
    def on_ui_text_entry_finish(self, *, ui_element, text):
        pass

    @delegate
    def on_ui_drop_down_menu_change(self, *, ui_element, option):
        pass

    @delegate
    def on_ui_textbox_link_click(self, *, ui_element, link_target):
        pass

    @delegate
    def on_ui_horizontal_slider_move(self, *, ui_element, slider_value):
        pass

    @delegate
    def on_ui_selection_list_new_selection(self, *, ui_element, selection):
        pass

    @delegate
    def on_ui_selection_list_drop_selection(self, *, ui_element, selection):
        pass

    @delegate
    def on_ui_window_close(self, *, ui_element):
        pass

    @delegate
    def on_ui_window_move_to_front(self, *, ui_element):
        pass

    @delegate
    def on_ui_confirmation_dialog_confirm(self, *, ui_element):
        pass

    @delegate
    def on_ui_file_dialog_path_pick(self, *, ui_element, filepath):
        pass
