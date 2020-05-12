import pygame


class CardView(pygame.sprite.Group):
    def __init__(self, cards, view_size, card_size, pos=(10, 10)):
        self.cards = cards
        self.width, self.height = view_size
        self.card_width, self.card_height = card_size
        self.x, self.y = pos
        self.dragging = False

        # determine the maximum number of cards that can appear on the screen at once
        self.max_visible = self.width // self.card_width

        # set the initial set of cards in the stack to be rendered
        self.visible = list(range(min(len(self.cards), self.max_visible)))

        super(CardView, self).__init__()

    def update(self, events, mouse_delta):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bar_rect = pygame.Rect(self.x, self.y, self.width, 30)
                    if bar_rect.collidepoint(*pygame.mouse.get_pos()):
                        self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging:
                    self.dragging = False

        if self.dragging:
            self.x += mouse_delta[0]
            self.y += mouse_delta[1]

    def draw(self, surface):
        view_bg = (242, 242, 242)
        bar_bg = (142, 142, 142)
        cross_color = (255, 0, 0)
        cross_line_width = 3
        bar_height = 30
        cross_buffer = 8

        view_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        bar_rect = pygame.Rect(self.x, self.y, self.width, bar_height)

        pygame.draw.rect(surface, view_bg, view_rect)
        pygame.draw.rect(surface, bar_bg, bar_rect)

        # draw the cross
        cross_width = bar_height - cross_buffer * 2
        cross_right_x = self.x + self.width - cross_buffer
        cross_left_x = cross_right_x - cross_width
        cross_top_y = self.y + cross_buffer
        cross_bottom_y = cross_top_y + cross_width
        pygame.draw.line(surface,
                         cross_color,
                         (cross_left_x, cross_top_y),
                         (cross_right_x, cross_bottom_y),
                         cross_line_width)
        pygame.draw.line(surface,
                         cross_color,
                         (cross_right_x, cross_top_y),
                         (cross_left_x, cross_bottom_y),
                         cross_line_width)



