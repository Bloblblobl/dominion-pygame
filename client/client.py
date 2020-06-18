from .object_model import (
    GameClient,
    Player,
    ClientEventHandler)


class Client(GameClient, Player):
    def __init__(self, client_event_handler: ClientEventHandler):
        self._state = None
        self.client_event_handler = client_event_handler
        self.game_events = []

    # GameClient interface implementation
    def play_action_card(self, card):
        pass

    def buy(self, card_type):
        pass

    def done(self):
        pass

    @property
    def state(self):
        return self._state

    # Player interface implementation
    def play(self):
        self.client_event_handler.on_play()

    def respond(self, action, *args):
        self.client_event_handler.on_respond()

    def on_event(self, event):
        self.game_events.append(event)

    # Triggered by server
    def on_state_change(self, state):
        self._state = state
