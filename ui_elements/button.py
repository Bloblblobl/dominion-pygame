import pygame

from constants import font_name

font_size = 15
font_color = (0, 0, 0)

class Button:
    def __init__(self, pos, width, height, color=(100,100,100), text=''):
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font = pygame.font.SysFont(font_name, font_size)
        self.rendered_text = self.font.render(self.text, False, font_color)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.rendered_text, (self.x, self.y))

    def update(self):
        # self.rendered_text = self.font.render(self.text, antialias=False, color=font_color)
        pass
