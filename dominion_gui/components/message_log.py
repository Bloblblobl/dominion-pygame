from dominion_gui.event_handler import EventHandler
from dominion_gui.ui_elements.html_textbox import HTMLTextBox
from dominion_gui.ui_util import (get_random_color, say)


class MessageLog(HTMLTextBox, EventHandler):
    def __init__(self, layout_info, container, bg_color=None, padding=None):
        super().__init__('', layout_info, container, bg_color, padding)
        self.messages = []
        self.players = {}
        self.subscribe(owner=None,
                       handler_name='on_custom_event',
                       subscriber=self)

    def format_message(self, message, mask=None):
        for player, color in self.players.items():
            message = message.replace(player, f'<font color={color}>{player}</font>')
        if mask is not None:
            try:
                message = mask.format(message)
            except Exception as e:
                pass
        return message

    def add_message(self, message, mask=None):
        formatted_message = self.format_message(message, mask)
        self.messages.append(formatted_message)
        self.html = '<br>'.join(self.messages)
        say(message)

    def on_custom_event(self, event):
        if isinstance(event, dict):
            if event['event'] == 'game start':
                self.add_message('Game Started!')
                self.add_message('Players:')
                for player in event['player_names']:
                    self.players[player] = get_random_color()
                    self.add_message(player)
                self.add_message('-' * 10)
            elif event['event'] == 'game over':
                self.add_message('-' * 10)
                self.add_message('Game Over!')
                self.add_message('-' * 10)
                winners = event['winners']
                if len(winners) == 1:
                    self.add_message(f'{winners[0]} won the game.')
                else:
                    self.add_message(f'the winners are: {", ".join(winners)}.')
                self.add_message('-' * 10)
                for player, score in event['scores'].items():
                    self.add_message(f'{player} has {score[0]} points and {score[1]} coins')

        elif isinstance(event, str):
            self.add_message(event)

        elif isinstance(event, list):
            self.add_message(*event)
