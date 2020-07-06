from client import object_model


class UIPlayer(object_model.Player):
    def __init__(self):
        self.state = None
        self.message_queue = []

    def play(self):
        pass

    def respond(self, action, *args):
        pass

    def on_game_event(self, event):
        self.message_queue.append(event)

    def on_state_change(self, state):
        self.state = state
