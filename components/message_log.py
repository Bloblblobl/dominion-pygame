import pygame

from constants import font_name

font_size = 15
font_color = (255, 255, 255)

log_width = 180
log_height = 300
log_color = (50, 50, 50)

scrollbar_width = 20
scrollbar_color = (230, 230, 230)
scroller_color = (150, 150, 150)

header_message = 'Events:'


class MessageLog:
    def __init__(self, messages, pos=(0, 0), width=log_width, height=log_height):
        self.messages = messages
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.text_width = self.width - scrollbar_width

        self.font = pygame.font.Font(font_name, font_size)
        _, self.font_height = self.font.size('how tall is this font?')

        self._render_text()

    @property
    def num_lines(self):
        return self.height // self.font_height

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def _split_message(self, message):
        # splits the message into multiple lines if the message is too long
        remaining_message = message
        split_message = []
        while remaining_message:
            i = len(remaining_message)
            while i > -1:
                new_message = remaining_message[:i]
                new_width, _ = self.font.size(new_message)
                if new_width <= self.text_width:
                    split_message.append(new_message)
                    remaining_message = remaining_message[i:]
                    if remaining_message and remaining_message[0] != '-':
                        remaining_message = '-' + remaining_message
                    break
                i -= 1

        return split_message

    def _render_text(self):
        self.rendered_header = self.font.render(header_message, False, font_color)

        rendered_text = []
        for message in self.messages:
            text_width, _ = self.font.size(message)
            if text_width > self.text_width:
                split_message = self._split_message(message)
                rendered_text.extend([self.font.render(m, False, font_color) for m in split_message])
            else:
                rendered_text.append(self.font.render(message, False, font_color))

        self.rendered_text = rendered_text

        self.message_index = max(0, len(self.rendered_text) - self.num_lines)
        self.max_index = self.message_index

    def _draw_scrollbar(self, surface):
        header_height = self.rendered_header.get_height()

        scrollbar_x = self.x + self.text_width
        scrollbar_y = self.y + header_height
        scrollbar_rect = (scrollbar_x, scrollbar_y, scrollbar_width, self.height)
        pygame.draw.rect(surface, scrollbar_color, scrollbar_rect)

        if len(self.rendered_text) <= self.num_lines:
            return

        scroller_x = scrollbar_x
        scroller_y = scrollbar_y + (self.height / len(self.rendered_text) * self.message_index)
        scroller_height = self.height * self.num_lines / len(self.rendered_text)
        scroller_rect = (scroller_x, scroller_y, scrollbar_width, scroller_height)
        pygame.draw.rect(surface, scroller_color, scroller_rect)

    def draw(self, surface):
        surface.blit(self.rendered_header, (self.x, self.y))

        text_x = self.x
        text_y = self.y + self.rendered_header.get_height()

        background_rect = (text_x, text_y, self.width, self.height)
        pygame.draw.rect(surface, log_color, background_rect)

        lines_to_draw = min(len(self.rendered_text[self.message_index:]), self.num_lines)
        for i in range(lines_to_draw):
            text = self.rendered_text[self.message_index + i]
            surface.blit(text, (text_x, text_y))
            text_y += text.get_height()
        self._draw_scrollbar(surface)

    def update(self, events, mouse_pos):
        if not self.rect.collidepoint(*mouse_pos):
            return
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_WHEELUP:
                    if self.message_index > 0:
                        self.message_index -= 1
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    if self.message_index < self.max_index:
                        self.message_index += 1
