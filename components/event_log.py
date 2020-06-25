import pygame

from constants import font_name

font_size = 15
font_color = (255, 255, 255)
log_width = 180
log_height = 300


class EventLog:
    def __init__(self, text, pos=(0, 0), width=log_width, height=log_height):
        self.text = text
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.font = pygame.font.Font(font_name, font_size)
        self.rendered_text = self._render_text()

    def _render_text(self):
        rendered_text = []
        i = len(self.text) - 1
        height_remaining = self.height

        while i > -1:
            text = self.text[i]
            _, text_height = self.font.size(text)
            if height_remaining < text_height:
                break
            rendered_text.append(self.font.render(text, False, font_color))
            height_remaining -= text_height
            i -= 1

        return list(reversed(rendered_text))

    def draw(self, surface):
        text_x = self.x
        text_y = self.y
        for text in self.rendered_text:
            surface.blit(text, (text_x, text_y))
            text_y += text.get_height()

    def update(self):
        pass
