from enum import Enum

MouseButton = Enum('MouseButton', 'Left Middle Right')


class EventHandler:
    '''PYGAME EVENTS

    https://www.pygame.org/docs/ref/event.html

    Events omitted:
    QUIT
    ACTIVEEVENT
    JOYAXISMOTION
    JOYBALLMOTION
    JOYHATMOTION
    JOYBUTTONUP
    JOYBUTTONDOWN
    VIDEORESIZE
    VIDEOEXPOSE
    '''

    def on_mouse_move(self, x, y):
        pass

    def on_mouse_button_down(self, button):
        pass

    def on_mouse_button_up(self, button):
        pass

    def on_mouse_scroll(self, direction):
        pass

    def on_key_down(self, key, modifiers):
        pass

    def on_key_up(self, key, modifiers):
        pass

    def on_mouse_enter(self, *, ui_element):
        pass

    def on_mouse_leave(self, *, ui_element):
        pass

    def on_click(self, *, ui_element):
        pass

    def on_custom_event(self, event):
        pass

    '''PYGAME GUI EVENTS

    https://pygame-gui.readthedocs.io/en/latest/events.html

    Events omitted:
    UI_BUTTON_DOUBLE_CLICKED
    UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION
    UI_COLOUR_PICKER_COLOUR_PICKED
    UI_COLOUR_PICKER_COLOUR_CHANNEL_CHANGED
    '''
    def on_ui_button_press(self, *, ui_element):
        pass

    def on_ui_text_entry_change(self, *, ui_element, text):
        pass

    def on_ui_text_entry_finish(self, *, ui_element, text):
        pass

    def on_ui_drop_down_menu_change(self, *, ui_element, option):
        pass

    def on_ui_textbox_link_click(self, *, ui_element, link_target):
        pass

    def on_ui_horizontal_slider_move(self, *, ui_element, slider_value):
        pass

    def on_ui_selection_list_new_selection(self, *, ui_element, selection):
        pass

    def on_ui_selection_list_drop_selection(self, *, ui_element, selection):
        pass

    def on_ui_window_close(self, *, ui_element):
        pass

    def on_ui_window_move_to_front(self, *, ui_element):
        pass

    def on_ui_confirmation_dialog_confirm(self, *, ui_element):
        pass

    def on_ui_file_dialog_path_pick(self, *, ui_element, filepath):
        pass
