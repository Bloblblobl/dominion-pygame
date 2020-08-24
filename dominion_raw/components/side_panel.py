import pygame

from dominion_raw.components.message_log import MessageLog
from dominion_raw.constants import screen_width, screen_height, card_spacing, font_name, WHITE, RED
from dominion_raw.ui_elements.button import Button
from dominion_object_model import object_model

font_size = 15
font_color = WHITE
active_player_color = RED
spacing_factor = 4
button_width = 180
button_height = 40

players_text = 'Players:'
action_text = 'Actions Remaining:'
buys_text = 'Buys Remaining:'
money_text = 'Money:'


class SidePanel:
    def __init__(self, pos, color, game_client: object_model.GameClient, players=None):
        self.x, self.y = pos
        self.width = screen_width - self.x
        self.height = screen_height - self.y
        self.card = None
        self.color = color
        self.font = pygame.font.Font(font_name, font_size)
        self.rect = pygame.Rect(*pos, self.width, self.height)

        self.game_client = game_client
        self.players = ['John', 'Johnny', 'Jonathan', 'Otter'] if players is None else players
        self.active_index = 1
        self.active_actions = 5
        self.active_buys = 3
        self.active_money = 2
        self._render_game_info_text()

        end_turn_pos = (
            self.x + self.width // 2 - button_width // 2,
            screen_height - button_height * 1.5
        )
        play_treasures_pos = (
            self.x + self.width // 2 - button_width // 2,
            screen_height - button_height * 3
        )
        self.end_turn_button = Button(end_turn_pos, button_width, button_height, text='END TURN',
                                      on_click=self._on_end_turn_click)
        self.play_treasures_button = Button(play_treasures_pos, button_width, button_height, text='PLAY ALL TREASURES',
                                            on_click=self._on_play_teasures_click)
        self.message_log = MessageLog([], width=self.width - card_spacing * 2)

    def _on_end_turn_click(self, source):
        self.game_client.done()

    def _on_play_teasures_click(self, source):
        pass

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
        self.rendered_game_info_text = rendered_text

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
        self.message_log.x = self.x + self.width // 2 - self.message_log.width // 2
        self.message_log.y = self._draw_game_info_text(surface, text_x, text_y) + spacing
        if self.card is not None:
            zoom_x = self.x + self.width // 2 - self.card.zoom.get_width() // 2
            zoom_y = self.message_log.y + (self.message_log.height // 2 - self.card.zoom.get_height() // 2)
            surface.blit(self.card.zoom, (zoom_x, zoom_y))
        else:
            self.message_log.draw(surface)
        self.end_turn_button.draw(surface)
        self.play_treasures_button.draw(surface)

    def update(self, events, mouse_pos, card):
        self.card = card
        self.message_log.update(events, mouse_pos)
        self._render_game_info_text()
        self.play_treasures_button.update()
        self.end_turn_button.update()
