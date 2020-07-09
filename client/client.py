from .object_model import (
    GameClient,
    Player,
    ClientEventHandler)

from PodSixNet.Connection import connection, ConnectionListener


class Client(ConnectionListener,
             GameClient,
             Player):
    def __init__(self, name, player: Player, host='127.0.0.1', port=5071):
        self.name = name
        self._player = player
        self.Connect((host, port))
        self.players = [name]
        self.card_names = []

    def pump(self):
        self.Pump()
        connection.Pump()

    def start_game(self):
        self.Send(dict(action='start'))

    # Player interface
    def play(self):
        self._player.play()
        # self.done()

    def respond(self, action, *args):
        response = self._player.respond(action, *args)
        self.Send(dict(action='respond', response=response))

    def on_game_event(self, event):
        self._player.on_game_event(event)

    def on_state_change(self, state):
        self._player.on_state_change(state)

    # GameClient interface
    def play_action_card(self, card):
        self.Send(dict(action='play_action_card', card=card))

    def buy(self, card_type):
        self.Send(dict(action='buy', card=card_type))

    def done(self):
        self.Send(dict(action='done'))

    # Server events
    def Network(self, data):
        print(data)

    def Network_on_player_join(self, data):
        self.players.append(data['name'])
        message = f'Player joined: {data["name"]}'
        self._player.on_game_event(message)

    def Network_on_game_start(self, data):
        card_names = data['card_names']
        player_names = data['player_names']
        message = f'Game started! cards={card_names}, players={player_names}'
        self.card_names = card_names
        self.players = player_names
        self._player.on_game_event(message)

    def Network_on_state(self, data):
        self.on_state_change(data['state'])

    def Network_on_game_event(self, data):
        self.on_game_event(data['event'])

    # Server commands
    def Network_play(self, data):
        self.play()

    def Network_respond(self, data):
        self.respond(data['action_card'], data['args'])

    # built in stuff
    def Network_connected(self, data):
        print("You are now connected to the server")
        self.Send(dict(action='join', name=self.name))

    def Network_error(self, data):
        print('error:', data['error'][1])
        connection.Close()

    def Network_disconnected(self, data):
        print('Server disconnected')
        exit()
