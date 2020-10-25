from dominion_gui.base_event_handler import BaseEventHandler
from dominion_gui.event_manager import get_event_manager
from dominion_gui.ui_elements.html_textbox import HTMLTextBox


class MessageLog(HTMLTextBox, BaseEventHandler):
    def __init__(self, layout_info, container, bg_color=None, padding=None):
        super().__init__('', layout_info, container, bg_color, padding)
        self.messages = []
        get_event_manager().subscribe(owner=None,
                                      handler_name='on_custom_event',
                                      subscriber=self)

    def add_message(self, message):
        self.messages.append(message)
        self.html = '<br>'.join(self.messages)

    def on_custom_event(self, event):
        if isinstance(event, dict):
            if event['event'] == 'game start':
                self.add_message('Game Started!')
                self.add_message('Players:')
                for player in event['player_names']:
                    self.add_message(player)
                self.add_message('-' * 10)
        else:
            self.add_message(str(event))