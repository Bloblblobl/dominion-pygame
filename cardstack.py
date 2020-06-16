import pygame


class CardStack:
    def __init__(self, cards, card_size, top_face_up=False, pos=(0, 0), x_spacing=1.5, y_spacing=2):
        self.card_width, self.card_height = card_size
        self.top_face_up = top_face_up
        self.cards = cards
        self.x, self.y = pos
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.max_stack = 20

    @property
    def width(self):
        return self.card_width + self.x_spacing * self.stack_size - 1

    @property
    def stack_size(self):
        return min(self.max_stack, len(self.cards))

    def draw(self, surface):
        card_x = self.x
        card_y = self.y

        for i in range(self.stack_size):
            self.cards[0].draw(surface, (card_x, card_y), False, self.top_face_up and i == self.stack_size - 1)
            card_x += self.x_spacing
            card_y += self.y_spacing

    def update(self):
        pass
