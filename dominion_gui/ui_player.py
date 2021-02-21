import pygame
from dominion_object_model import object_model

from dominion_gui.card_manifest import create_card_manifest
from dominion_gui.event_handler import EventHandler
from dominion_gui.event_manager import get_event_manager, ResponseEvent
from dominion_gui.responder import Responder

your_turn_message = ['Your turn!', '<font color=#7df9ff>{}</font>']


class UIPlayer(object_model.Player, EventHandler):
    instance = None

    def __init__(self, game_client):
        self.game_client = game_client
        self.state = None
        self.pending_response = None
        get_event_manager().subscribe(None, 'on_custom_event', self)

    def play(self):
        your_turn_event = pygame.event.Event(
            pygame.USEREVENT,
            dict(user_type='custom_event', event=your_turn_message)
        )
        pygame.event.post(your_turn_event)

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        em = get_event_manager()
        em.on_custom_event(event)

    def on_state_change(self, state):
        self.state = state

    def on_custom_event(self, event):
        if isinstance(event, dict):
            if 'event' in event and event['event'] == 'game start':
                card_manifest_dict = {key: value for key, value in event.items() if
                                      key not in ('event', 'player_names')}
                create_card_manifest(card_manifest_dict)
            return

        if not isinstance(event, ResponseEvent):
            return

        self.game_client.respond(event.action, event.response)
        Responder.get_instance().cleanup()
