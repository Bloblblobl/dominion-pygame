import pygame

from constants import screen_width, screen_height, card_spacing


class SidePanel:
    def __init__(self, pos=(0, 0), color=(0, 0, 0)):
        self.x, self.y = pos
        self.width = screen_width - self.x
        self.height = screen_height - self.y
        self.card = None
        self.color = color
        self.rect = pygame.Rect(*pos, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        if self.card is not None:
            surface.blit(self.card.zoom,
                         (self.x + self.width // 2 - self.card.zoom.get_width() // 2, self.y + card_spacing * 4))

    def update(self, card):
        self.card = card