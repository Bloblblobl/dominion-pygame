import pygame

from constants import font_name

font_size = 16
font_color = (0, 0, 0)


class Button:
    def __init__(self, pos, width, height, color=(100,100,100), text=''):
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font = pygame.font.Font(font_name, font_size)
        self.rendered_text = self.font.render(self.text, False, font_color)

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_x = self.x + self.width // 2 - self.rendered_text.get_width() // 2
        text_y = self.y + self.height // 2 - self.rendered_text.get_height() // 2
        surface.blit(self.rendered_text, (text_x, text_y))

    def update(self):
        # self.rendered_text = self.font.render(self.text, antialias=False, color=font_color)
        pass
