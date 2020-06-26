import pygame

from components.message_log import MessageLog
from constants import screen_width, screen_height, card_spacing, font_name
from ui_elements.button import Button

font_size = 15
font_color = (255, 255, 255)
active_player_color = (255, 0, 0)
spacing_factor = 4
button_width = 180
button_height = 40

players_text = 'Players:'
action_text = 'Actions Remaining:'
buys_text = 'Buys Remaining:'
money_text = 'Money:'

test_log_text = [
    '[player] bought [card]',
    '[player] played [card]',
    '[player] discarded [#] cards',
    'Guy lost the game!',
    'What\'s this?',
    'Guy seems to keep losing',
    'over and over and over again!',
    'Wow, what a loser',
    'Wait a second!',
    'I think he\'s actually winning!',
    'JK he lost again haha',
    'This is a super super super duper super duper pooper scooper cooper hooper stupor long line, and guess what? It\'s even longer than that!'
]


class SidePanel:
    def __init__(self, pos=(0, 0), color=(0, 0, 0), players=None):
        self.x, self.y = pos
        self.width = screen_width - self.x
        self.height = screen_height - self.y
        self.card = None
        self.color = color
        self.font = pygame.font.Font(font_name, font_size)
        self.rect = pygame.Rect(*pos, self.width, self.height)

        self.players = ['John', 'Johnny', 'Jonathan', 'Otter'] if players is None else players
        self.active_index = 1
        self.active_actions = 5
        self.active_buys = 3
        self.active_money = 2
        self.rendered_game_info_text = self._render_game_info_text()

        end_turn_pos = (
            self.x + self.width // 2 - button_width // 2,
            screen_height - button_height * 1.5
        )
        play_treasures_pos = (
            self.x + self.width // 2 - button_width // 2,
            screen_height - button_height * 3
        )
        self.end_turn_button = Button(end_turn_pos, button_width, button_height, text='END TURN')
        self.play_treasures_button = Button(play_treasures_pos, button_width, button_height, text='PLAY ALL TREASURES')
        self.event_log = MessageLog(test_log_text, width=self.width - card_spacing * 2)

    def _render_game_info_text(self):
        rendered_text = []
        rendered_text.append(self.font.render(players_text, False, font_color))
        for i, player in enumerate(self.players):
            player_color = active_player_color if self.active_index == i else font_color
            player_prefix = ' > ' if self.active_index == i else '    '
            rendered_text.append(self.font.render(f'{player_prefix}{player}', False, player_color))
        rendered_text.append(self.font.render(f'{action_text} {self.active_actions}', False, font_color))
        rendered_text.append(self.font.render(f'{buys_text} {self.active_buys}', False, font_color))
        rendered_text.append(self.font.render(f'{money_text} {self.active_money}', False, font_color))
        return rendered_text

    def _draw_game_info_text(self, surface, text_x, text_y):
        for text in self.rendered_game_info_text:
            surface.blit(text, (text_x, text_y))
            text_y += text.get_height()
        return text_y

    def draw(self, surface):
        spacing = card_spacing * spacing_factor
        text_x = self.x + spacing
        text_y = self.y + spacing
        pygame.draw.rect(surface, self.color, self.rect)
        self.event_log.x = self.x + self.width // 2 - self.event_log.width // 2
        self.event_log.y = self._draw_game_info_text(surface, text_x, text_y) + spacing
        if self.card is not None:
            zoom_x = self.x + self.width // 2 - self.card.zoom.get_width() // 2
            zoom_y = self.event_log.y + (self.event_log.height // 2 - self.card.zoom.get_height() // 2)
            surface.blit(self.card.zoom, (zoom_x, zoom_y))
        else:
            self.event_log.draw(surface)
        self.end_turn_button.draw(surface)
        self.play_treasures_button.draw(surface)

    def update(self, card):
        self.card = card