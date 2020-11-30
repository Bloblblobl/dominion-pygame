from dominion_gui.event_handler import EventHandler
from dominion_gui.ui_elements.html_textbox import HTMLTextBox


class MessageLog(HTMLTextBox, EventHandler):
    def __init__(self, layout_info, container, bg_color=None, padding=None):
        super().__init__('', layout_info, container, bg_color, padding)
        self.messages = []
        self.subscribe(owner=None,
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
        elif isinstance(event, str):
            self.add_message(event)
