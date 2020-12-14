from time import sleep

from dominion_object_model import object_model

from dominion_gui.event_handler import EventHandler
from dominion_gui.event_manager import get_event_manager, ResponseEvent
from dominion_gui.responder import Responder


class UIPlayer(object_model.Player, EventHandler):
    instance = None

    def __init__(self, game_client):
        self.game_client = game_client
        self.state = None
        self.pending_response = None
        get_event_manager().subscribe(None, 'on_custom_event', self)

    def play(self):
        pass

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        em = get_event_manager()
        em.on_custom_event(event)

    def on_state_change(self, state):
        self.state = state

    def on_custom_event(self, event):
        if not isinstance(event, ResponseEvent):
            return

        self.game_client.respond(event.action, event.response)
        Responder.get_instance().cleanup()
