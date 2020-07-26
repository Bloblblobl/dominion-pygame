from pygame_gui import UIManager

from dominion_gui.constants import theme_path

manager = None


def get_manager(screen_size=None):
    return _get_manager(screen_size)


def _get_manager(screen_size):
    return __get_manager(screen_size)


def __get_manager(screen_size):
    global manager
    global _get_manager
    manager = UIManager(screen_size, theme_path=theme_path)
    _get_manager = lambda x: manager
    return manager