import pygame


class CardStack:
    def __init__(self, cards, card_size, top_face_up=False, pos=(0, 0), spacing=2):
        self.card_width, self.card_height = card_size
        self.top_face_up = top_face_up
        self.cards = cards
        self.x, self.y = pos
        self.spacing = spacing

    def draw(self, surface):
        card_x = self.x
        card_y = self.y

        for i in range(len(self.cards)):
            self.cards[0].draw(surface, (card_x, card_y), False)
            card_x += self.spacing
            card_y += self.spacing

    def update(self):
        pass
