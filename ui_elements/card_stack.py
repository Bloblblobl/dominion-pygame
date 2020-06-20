import pygame

from constants import card_size


class CardStack:
    def __init__(self,
                 cards,
                 top_face_up=False,
                 pos=(0, 0),
                 x_spacing=3.75,
                 y_spacing=5,
                 on_click=lambda card_view: None):
        self.card_width, self.card_height = card_size
        self.top_face_up = top_face_up
        self.cards = cards
        self.x, self.y = pos
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.max_stack = 8
        self.max_width = self.card_width + self.x_spacing * self.max_stack - 1
        self.max_height = self.card_height + self.y_spacing * self.max_stack - 1
        self.rect = pygame.Rect(self.x, self.y, self.max_width, self.max_height)
        self.on_click = on_click

    @property
    def stack_size(self):
        return min(self.max_stack, len(self.cards))

    @property
    def width(self):
        return self.card_width + self.x_spacing * self.stack_size - 1

    @property
    def height(self):
        return self.card_height + self.y_spacing * self.stack_size - 1

    def draw(self, surface):
        card_x = self.x
        card_y = self.y

        for i in range(self.stack_size):
            self.cards[0].draw(surface,
                               (card_x, card_y),
                               selected=False,
                               face_up=self.top_face_up and i == self.stack_size - 1)
            card_x += self.x_spacing
            card_y += self.y_spacing

    def update(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if self.rect.collidepoint(*mouse_pos):
                        self.on_click(self)