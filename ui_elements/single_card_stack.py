import pygame

from constants import card_size


class SingleCardStack:
    def __init__(self,
                 card,
                 count,
                 pos=(0, 0),
                 x_spacing=3.75,
                 y_spacing=5,
                 on_click=lambda source: None):
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
        self.state = 'normal'
        self.on_click = on_click

    @property
    def stack_size(self):
        return min(self.max_stack, self.count)

    @property
    def width(self):
        return self.card_width + self.x_spacing * self.stack_size - 1

    @property
    def height(self):
        return self.card_height + self.y_spacing * self.stack_size - 1

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, disabled=False):
        card_x = self.x
        card_y = self.y

        for i in range(self.stack_size):
            if self.state == 'hover' and i == self.stack_size - 1:
                border_rect = (card_x, card_y, self.card.width + 4, self.card.height + 4)
                pygame.draw.rect(surface, (255, 0, 0), border_rect)
            self.card.draw(surface, (card_x, card_y), selected=False, face_up=True, disabled=disabled)
            card_x += self.x_spacing
            card_y += self.y_spacing

    def update(self):
        pass

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