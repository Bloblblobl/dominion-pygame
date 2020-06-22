import pygame

from constants import screen_width, screen_height, card_spacing
from ui_elements.button import Button


class SidePanel:
    def __init__(self, pos=(0, 0), color=(0, 0, 0), players=None):
        self.x, self.y = pos
        self.width = screen_width - self.x
        self.height = screen_height - self.y
        self.card = None
        self.color = color
        self.rect = pygame.Rect(*pos, self.width, self.height)
        self.button = Button(pos, 125, 75, text='TEST')

        self.players = ['John', 'Johnny', 'Jonathan', 'Fergusontile'] if players is None else players
        self.active_index = -1
        self.active_actions = 5
        self.active_buys = 3
        self.active_money = 2

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.card is not None:
            surface.blit(self.card.zoom,
                         (self.x + self.width // 2 - self.card.zoom.get_width() // 2, self.y + card_spacing * 4))
        self.button.draw(surface)

    def update(self, card):
        self.card = card
        if card is not None:
            self.button.x = self.x + self.width // 2 - self.card.zoom.get_width() // 2
            self.button.y = self.y + self.card.zoom.get_height() + card_spacing * 8