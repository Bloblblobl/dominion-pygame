from dominion_object_model.object_model import Player, GameClient
from dominion_grpc_client.client import Client as GRPCClient


from ui_player import UIPlayer


class Client:
    def __init__(self, name, player_factory):
        self.grpc_client = GRPCClient(name, player_factory)

    def start_game(self):
        self.grpc_client.start_game()

    # Player interface
    def play(self):
        UIPlayer.instance.play()

    def respond(self, action, *args):
        response = UIPlayer.instance.respond(action, *args)
        self.grpc_client.Respond()

    # def on_game_event(self, event):
    #     pass
    #
    # def on_state_change(self, state):
    #     pass

    # GameClient interface
    def play_action_card(self, card):
        self.Send(dict(action='play_action_card', card=card))

    def buy(self, card_type):
        self.Send(dict(action='buy', card=card_type))

    def done(self):
        self.Send(dict(action='done'))


# if __name__ == '__main__':
#     GRPCClient('dummy', DummyPlayer).run()
#     # GRPCClient('dummy', DummyPlayer).run(host='35.202.145.215')
