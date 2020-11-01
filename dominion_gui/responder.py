responder = None


def get_responder():
    return _get_responder()


def _get_responder():
    return __get_responder()


def __get_responder():
    global responder
    global _get_responder
    responder = Responder()
    _get_responder = lambda x: responder
    return responder


class ResponseEvent:
    def __init__(self, response):
        self.response = response


class Responder:
    def handle(self, action, *args):
        handler = getattr(self, 'handle_' + action)
        return handler(*args)

    def handle_militia(self):
        pass