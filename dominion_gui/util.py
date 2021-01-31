import re
from typing import Union, List
from types import SimpleNamespace

from dominion_gui.card_manifest import get_card_manifest


def Noneable(t):
    return Union[t, None]


def get_card_class(card_name: str) -> str:
    return ''.join([word.capitalize() for word in card_name.split('_')])


def get_card_name(card_class: str) -> str:
    return '_'.join(re.findall('[A-Z][^A-Z]*', card_class)).lower()


def get_card_data(card_name: str):
    card_manifest = get_card_manifest()
    if card_manifest is None:
        return None

    return card_manifest['card_types'][get_card_class(card_name)]


# filter_exp is a string that will be passed into eval
# use 'card.property' with a comparison
# example : "card.cost <= 5"
def filter_card_names(card_names: List[str], filter_exp: str) -> List[str]:
    card_manifest = get_card_manifest()
    if card_manifest is None:
        return card_names
    card_types = card_manifest['card_types']

    filtered_card_names = []
    for card_name in card_names:
        card_data = card_types[get_card_class(card_name)]
        card = SimpleNamespace(**{key.lower(): value for key, value in card_data.items()})
        try:
            result = eval(filter_exp)
        except:
            raise RuntimeError(f'Invalid filter expression in util.filter_card_names: {filter_exp}')

        if result:
            filtered_card_names.append(card_name)

    return filtered_card_names