import pygame


class CardView(pygame.sprite.Group):
    view_bg = (242, 242, 242)
    bar_bg = (200, 200, 200)
    cross_color = (255, 0, 0)
    cross_line_width = 3
    bar_height = 30
    cross_buffer = 8

    def __init__(self, cards, num_cards_visible, card_size, pos=(10, 10), spacing=15):
        self.cards = cards
        self.spacing = spacing
        self.card_width, self.card_height = card_size
        self.calculate_card_view_size(num_cards_visible)
        self.x, self.y = pos
        self.dragging = False
        self.num_cards_visible = num_cards_visible
        self.start_index = 0

        # set the initial set of cards in the card_view to be rendered
        self.visible = list(range(min(len(self.cards), num_cards_visible)))

        super(CardView, self).__init__()

    def update(self, events, mouse_delta):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    bar_rect = pygame.Rect(self.x, self.y, self.width, self.bar_height)
                    if bar_rect.collidepoint(*pygame.mouse.get_pos()):
                        self.dragging = True
                if event.button == pygame.BUTTON_WHEELUP:
                    if self.start_index > 0:
                        self.start_index -= 1
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    if self.start_index < len(self.cards) - self.num_cards_visible:
                        self.start_index += 1
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

        if self.dragging:
            self.x += mouse_delta[0]
            self.y += mouse_delta[1]

    def _draw_cross(self, surface, bar_height, line_width, buffer, color):
        cross_width = bar_height - buffer * 2
        cross_right_x = self.x + self.width - buffer
        cross_left_x = cross_right_x - cross_width
        cross_top_y = self.y + buffer
        cross_bottom_y = cross_top_y + cross_width
        pygame.draw.line(surface,
                         color,
                         (cross_left_x, cross_top_y),
                         (cross_right_x, cross_bottom_y),
                         line_width)
        pygame.draw.line(surface,
                         color,
                         (cross_right_x, cross_top_y),
                         (cross_left_x, cross_bottom_y),
                         line_width)

    def calculate_card_view_size(self, num_cards):
        self.width = self.spacing + num_cards * (self.card_width + self.spacing)
        self.height = (self.spacing * 2) + self.bar_height + self.card_height

    def draw(self, surface):


        view_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        bar_rect = pygame.Rect(self.x, self.y, self.width, self.bar_height)

        # draw the bachground of the view
        pygame.draw.rect(surface, self.view_bg, view_rect)

        # draw the drag bar of the view
        pygame.draw.rect(surface, self.bar_bg, bar_rect)

        # draw the cross
        self._draw_cross(surface, self.bar_height, self.cross_line_width, self.cross_buffer, self.cross_color)

        # draw the cards

        # if there are cards (otherwise do nothing)
        #   1. calculate how many cards can fit in the view => n
        #   2. calculate the position to draw the first card
        #   3. loop over the first n cards (or all cards if len(cards) <= n)
        #   4. for each card
        #       a. draw the card
        #       b. update the position for the next card

        if not self.cards:
            return

        card_width = self.cards[0].width
        num_cards = (self.width - self.spacing) // (card_width + self.spacing)
        card_x = self.x + self.spacing
        card_y = self.y + self.bar_height + self.spacing
        for i in range(self.start_index, self.start_index + self.num_cards_visible):
            self.cards[i].draw(surface, (card_x, card_y), False)
            card_x += card_width + self.spacing
