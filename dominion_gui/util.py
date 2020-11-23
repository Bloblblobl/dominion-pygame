from typing import Union

import re

from dominion_gui.components.default import get_default_layout
from dominion_gui.ui_elements.label import Label


dummy = None


def Noneable(t):
    return Union[t, None]


def calculate_text_size(text, padding):
    global dummy
    if dummy is None:
        dummy = Label('', get_default_layout(), None).element
    return (x + padding for x in dummy.font.size(text))


def get_card_class(card_name: str) -> str:
    return ''.join([word.capitalize() for word in card_name.split('_')])


def get_card_name(card_class: str) -> str:
    return '_'.join(re.findall('[A-Z][^A-Z]*', card_class)).lower()