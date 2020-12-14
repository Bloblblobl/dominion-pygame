import multiprocessing as mp

from dominion_grpc_client.client import Client as GRPCClient
from dominion_object_model import object_model


def get_instance():
    if GameClient.instance is None:
        GameClient.instance = GameClient()

    return GameClient.instance


class GameClient(object_model.GameClient):
    instance = None

    def __init__(self, name='test'):
        self._in_queue = mp.Queue()
        self._out_queue = mp.Queue()
        self._out_response_queue = mp.Queue()
        self._grpc_client = GRPCClient(name, self._in_queue, self._out_queue, self._out_response_queue)

    def connect(self, host, port):
        mp.Process(target=self._grpc_client.run, args=(host, port)).start()

    def get_message(self):
        """Get message from queue (non-blocking)"""
        if self._in_queue.empty():
            return None
        return self._in_queue.get()

    def start_game(self):
        self._out_queue.put(('start_game', None))

    def respond(self, action, *args):
        print(f'**** GameClient.respond({action}, {args}) - puts in out response queue')
        self._out_response_queue.put(('respond', (action, *args)))

    # GameClient interface
    def play_action_card(self, card_name: str):
        self._out_queue.put(('play_action_card', card_name))

    def buy(self, card_name: str):
        self._out_queue.put(('buy', card_name))

    def done(self):
        self._out_queue.put(('done', None))
