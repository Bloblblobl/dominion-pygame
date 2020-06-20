import pygame

from constants import card_size


class SingleCardStack:
    def __init__(self,
                 card,
                 count,
                 pos=(0, 0),
                 x_spacing=3.75,
                 y_spacing=5):
        self.card_width, self.card_height = card_size
        self.card = card
        self.count = count
        self.x, self.y = pos
        self.x_spacing = x_spacing
        self.y_spacing = y_spacing
        self.max_stack = 5
        self.max_width = self.card_width + self.x_spacing * self.max_stack - 1
        self.max_height = self.card_height + self.y_spacing * self.max_stack - 1
        self.rect = pygame.Rect(self.x, self.y, self.max_width, self.max_height)

    @property
    def stack_size(self):
        return min(self.max_stack, self.count)

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
            self.card.draw(surface, (card_x, card_y), selected=False, face_up=True)
            card_x += self.x_spacing
            card_y += self.y_spacing

    def update(self):
        pass