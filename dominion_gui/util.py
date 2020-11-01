from typing import Union

import re


def Noneable(t):
    return Union[t, None]


def get_card_class(card_name: str) -> str:
    return ''.join([word.capitalize() for word in card_name.split('_')])


def get_card_name(card_class: str) -> str:
    return '_'.join(re.findall('[A-Z][^A-Z]*', card_class)).lower()