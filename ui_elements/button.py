import pygame

from constants import font_name

font_size = 16
font_color = (0, 0, 0)


class Button:
    def __init__(self, pos, width, height, color=(100, 100, 100), text='', on_click=lambda source: None):
        self.x, self.y = pos
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.font = pygame.font.Font(font_name, font_size)
        self.rendered_text = self.font.render(self.text, False, font_color)
        self.state = 'normal'
        self.on_click = on_click

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
        if self.state == 'hover':
            self.color = (150, 150, 150)
        elif self.state == 'pressed':
            self.color = (200, 200, 200)
        else:
            self.color = (100, 100, 100)

    def handle_mouse_event(self, event_type, pos):
        if event_type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif event_type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif event_type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.rect.collidepoint(*pos):
            if self.state != 'pressed':
                self.state = 'hover'
        else:
            self.state = 'normal'

    def handle_mouse_down(self, pos):
        if self.rect.collidepoint(*pos):
            print('pressed')
            self.state = 'pressed'

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            print('mouse up')
            self.on_click(self)
            self.state = 'hover'

