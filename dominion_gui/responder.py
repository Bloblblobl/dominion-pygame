from dominion_gui import util
from dominion_gui.components.responses.artisan_response import ArtisanResponse
from dominion_gui.components.responses.bandit_response import BanditResponse
from dominion_gui.components.responses.cellar_response import CellarResponse
from dominion_gui.components.responses.chapel_response import ChapelResponse
from dominion_gui.components.responses.harbinger_response import HarbingerResponse
from dominion_gui.components.responses.militia_response import MilitiaResponse
from dominion_gui.components.responses.mine_response import MineResponse
from dominion_gui.components.responses.remodel_response import RemodelResponse
from dominion_gui.components.responses.sentry_response import SentryResponse
from dominion_gui.components.responses.throne_room_response import ThroneRoomResponse
from dominion_gui.components.responses.vassal_response import VassalResponse
from dominion_gui.components.responses.workshop_response import WorkshopResponse

tab_button_width = 100


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

    def handle_artisan(self, state, *args):
        supply_card_names = [util.get_card_name(card_name) for card_name in state['supply']]
        hand_card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=ArtisanResponse,
                                   supply_card_names=supply_card_names,
                                   hand_card_names=hand_card_names)
        self.tab_container.select_tab(name='Response')

    def handle_bandit(self, state, *args):
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=BanditResponse,
                                   card_names=args[0])
        self.tab_container.select_tab(name='Response')

    def handle_cellar(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=CellarResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def handle_chapel(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=ChapelResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def handle_harbinger(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['discard_pile']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=HarbingerResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def handle_militia(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=MilitiaResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def handle_mine(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=MineResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def handle_remodel(self, state, *args):
        supply_card_names = [util.get_card_name(card_name) for card_name in state['supply']]
        hand_card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=RemodelResponse,
                                   supply_card_names=supply_card_names,
                                   hand_card_names=hand_card_names)
        self.tab_container.select_tab(name='Response')

    def handle_sentry(self, state, *args):
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=SentryResponse,
                                   card_names=args[0])
        self.tab_container.select_tab(name='Response')

    def handle_throneroom(self, state, *args):
        card_names = [util.get_card_name(card['name']) for card in state['hand']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=ThroneRoomResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def handle_vassal(self, state, *args):
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=VassalResponse,
                                   card_names=args)
        self.tab_container.select_tab(name='Response')

    def handle_workshop(self, state, *args):
        card_names = [util.get_card_name(card_name) for card_name in state['supply']]
        self.tab_container.add_tab(name='Response',
                                   tab_button_width=tab_button_width,
                                   tab_factory=WorkshopResponse,
                                   card_names=card_names)
        self.tab_container.select_tab(name='Response')

    def cleanup(self):
        self.tab_container.remove_tab(name='Response', new_active='Play Area')
