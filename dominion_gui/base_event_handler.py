from enum import Enum

MouseButton = Enum('MouseButton', 'Left Middle Right')

class BaseEventHandler:
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

    '''PYGAME GUI EVENTS

    https://pygame-gui.readthedocs.io/en/latest/events.html

    Events omitted:
    UI_BUTTON_DOUBLE_CLICKED
    UI_SELECTION_LIST_DOUBLE_CLICKED_SELECTION
    UI_COLOUR_PICKER_COLOUR_PICKED
    UI_COLOUR_PICKER_COLOUR_CHANNEL_CHANGED
    '''
    def on_ui_button_pressed(self, *, ui_element):
        pass

    def on_ui_button_hovered(self, *, ui_element):
        pass

    def on_ui_button_unhovered(self, *, ui_element):
        pass

    def on_ui_text_entry_changed(self, *, ui_element, text):
        pass

    def on_ui_text_entry_finished(self, *, ui_element, text):
        pass

    def on_ui_drop_down_menu_changed(self, *, ui_element, option):
        pass

    def on_ui_textbox_link_clicked(self, *, ui_element, link_target):
        pass

    def on_ui_horizontal_slider_moved(self, *, ui_element, slider_value):
        pass

    def on_ui_selection_list_new_selection(self, *, ui_element, selection):
        pass

    def on_ui_selection_list_dropped_selection(self, *, ui_element, selection):
        pass

    def on_ui_window_closed(self, *, ui_element):
        pass

    def on_ui_window_moved_to_front(self, *, ui_element):
        pass

    def on_ui_confirmation_dialog_confirmed(self, *, ui_element):
        pass

    def on_ui_file_dialog_path_picked(self, *, ui_element, filepath):
        pass
