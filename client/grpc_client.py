from dominion_object_model.object_model import Player
from dominion_grpc_client.client import Client as GRPCClient


class DummyPlayer(Player):
    def __init__(self, game_client):
        self.game_client = game_client

    def play(self):
        self.game_client.done()

    def respond(self, action, *args):
        self.game_client.respond(action, 'dummy')

    def on_game_event(self, event):
        print(event)

    def on_state_change(self, state):
        pass

if __name__ == '__main__':
    GRPCClient('dummy', DummyPlayer).run()
    #GRPCClient('dummy', DummyPlayer).run(host='35.202.145.215')
