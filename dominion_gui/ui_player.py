from dominion_object_model import object_model

from dominion_gui.event_manager import get_event_manager


class UIPlayer(object_model.Player):
    instance = None

    def __init__(self, game_client):
        self.game_client = game_client
        self.state = None
        UIPlayer.instance = self

    def play(self):
        pass

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        em = get_event_manager()
        em.on_custom_event(event)

    def on_state_change(self, state):
        self.state = state
