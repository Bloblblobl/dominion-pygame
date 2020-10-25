from typing import Union

from threading import Thread

import time

from dominion_object_model import object_model
from dominion_grpc_client.client import Client as GRPCClient

from dominion_gui.ui_player import UIPlayer

instance = None


def connect():
    global instance

    instance = GRPCClient('test', UIPlayer)

    Thread(target=instance.run).start()
    game_started = False
    while not game_started:
        try:
            instance.start_game()
            game_started = True
        except:
            time.sleep(0.1)


def Noneable(t):
    return Union[t, None]


def get_instance() -> Noneable(object_model.GameClient):
    return instance
