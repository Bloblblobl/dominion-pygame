from dominion_object_model import object_model


class UIPlayer(object_model.Player):
    instance = None

    def __init__(self, game_client):
        self.game_client = game_client
        self.state = None
        self.message_queue = []
        UIPlayer.instance = self

    def play(self):
        pass

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        self.message_queue.append(str(event))

    def on_state_change(self, state):
        self.state = state
