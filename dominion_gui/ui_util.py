from dominion_gui.components.default import get_default_layout
from dominion_gui.ui_elements.label import Label

dummy = None


def calculate_text_size(text, padding):
    global dummy
    if dummy is None:
        dummy = Label('', get_default_layout(), None).element
    return (x + padding for x in dummy.font.size(text))
