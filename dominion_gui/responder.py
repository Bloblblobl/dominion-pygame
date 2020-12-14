from dominion_gui import util
from dominion_gui.components.responses.cellar_response import CellarResponse
from dominion_gui.components.responses.chapel_response import ChapelResponse
from dominion_gui.components.responses.harbinger_response import HarbingerResponse
from dominion_gui.components.responses.militia_response import MilitiaResponse


class Responder:
    instance = None

    @classmethod
    def create(cls, tab_container):
        if cls.instance is not None:
            raise Exception('Responder has already been created')
        cls.instance = Responder(tab_container)

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            raise Exception('Responder has not been created yet')
        return cls.instance

    def __init__(self, tab_container):
        self.tab_container = tab_container

    def handle(self, action, state, *args):
        handler = getattr(self, 'handle_' + action.lower())
        return handler(state, *args)

    def handle_militia(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=100,
                                   tab_factory=MilitiaResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def handle_cellar(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=100,
                                   tab_factory=CellarResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def handle_chapel(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=100,
                                   tab_factory=ChapelResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def handle_harbinger(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['discard_pile']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=100,
                                   tab_factory=HarbingerResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def cleanup(self):
        self.tab_container.remove_tab(name='Response', new_active='Play Area')
