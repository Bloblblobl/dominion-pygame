from client import object_model


class UIPlayer(object_model.Player):
    def __init__(self):
        self.state = None

    def play(self):
        pass

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        pass

    def on_state_change(self, state):
        self.state = state