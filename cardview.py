import pygame


class CardView(pygame.sprite.Group):
    view_bg = (242, 242, 242)
    dragbar_bg = (200, 200, 200)
    scrollbar_bg = (230, 230, 230)
    cross_color = (255, 0, 0)
    cross_line_width = 3
    bar_height = 30
    cross_buffer = 8
    scrollbar_height = 15

    def __init__(self, cards, num_cards_visible, card_size, pos=(10, 10), spacing=15, draggable=False, on_click=None):
        self.cards = cards
        self.spacing = spacing
        self.card_width, self.card_height = card_size
        self.draggable = draggable
        if not self.draggable:
            self.bar_height = 0
        self._calculate_card_view_size(num_cards_visible)
        self.x, self.y = pos
        self.dragging = False
        self.num_cards_visible = num_cards_visible
        self.start_index = 0
        self.card_rects = []
        self.selected_index = None
        self.on_click = on_click

        # set the initial set of cards in the card_view to be rendered
        self.visible = list(range(min(len(self.cards), num_cards_visible)))

        super(CardView, self).__init__()

    @property
    def cardview_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def _calculate_card_view_size(self, num_cards):
        self.width = self.spacing + num_cards * (self.card_width + self.spacing)
        self.height = (self.spacing * 3) + self.bar_height + self.card_height + self.scrollbar_height

    def _calculate_selected_card(self, mouse_pos):
        for i, card_rect in enumerate(self.card_rects):
            if card_rect.collidepoint(*mouse_pos):
                self.selected_index = i
                return
        self.selected_index = None

    @property
    def selected_card(self):
        return None if self.selected_index is None else self.cards[self.selected_index + self.start_index]

    def update(self, events, mouse_pos, mouse_delta):
        # TODO: Fix ugly nested ifs
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if self.draggable:
                        bar_rect = pygame.Rect(self.x, self.y, self.width, self.bar_height)
                        if bar_rect.collidepoint(*pygame.mouse.get_pos()):
                            self.dragging = True
                    if self.selected_card is not None and self.on_click is not None:
                        self.on_click(self)
                if not self.cardview_rect.collidepoint(*mouse_pos):
                    continue
                if event.button == pygame.BUTTON_WHEELUP:
                    if self.start_index > 0:
                        self.start_index -= 1
                elif event.button == pygame.BUTTON_WHEELDOWN:
                    if self.start_index < len(self.cards) - self.num_cards_visible:
                        self.start_index += 1
            elif event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False
                self.card_rects = []

        self._calculate_selected_card(mouse_pos)

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

    def _draw_cards(self, surface):
        # if there are cards (otherwise do nothing)
        #   1. calculate how many cards can fit in the view => n
        #   2. calculate the position to draw the first card
        #   3. loop over the first n cards (or all cards if len(cards) <= n)
        #   4. for each card
        #       a. draw the card
        #       b. update the position for the next card
        card_x = self.x + self.spacing
        card_y = self.y + self.spacing + self.bar_height
        generate_rects = self.card_rects == []

        end_index = min(len(self.cards), self.start_index + self.num_cards_visible)
        for i in range(self.start_index, end_index):
            draw_border = i - self.start_index == self.selected_index
            self.cards[i].draw(surface, (card_x, card_y), draw_border)
            if generate_rects:
                self.card_rects.append(pygame.Rect(card_x, card_y, self.card_width, self.card_height))
            card_x += self.card_width + self.spacing

    def _draw_scrollbar(self, surface):
        bar_x = self.x + self.spacing
        bar_y = self.y + self.bar_height + self.card_height + self.spacing * 2
        bar_width = self.width - self.spacing * 2
        bar_height = self.scrollbar_height
        bar_color = self.scrollbar_bg
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(surface, bar_color, bar_rect)

        if len(self.cards) <= self.num_cards_visible:
            return
        scroller_x = bar_x + (bar_width / len(self.cards) * self.start_index)
        scroller_y = bar_y
        scroller_width = bar_width * self.num_cards_visible / len(self.cards)
        scroller_height = bar_height
        scroller_color = self.dragbar_bg
        scroller_rect = pygame.Rect(scroller_x, scroller_y, scroller_width, scroller_height)
        pygame.draw.rect(surface, scroller_color, scroller_rect)

    def draw(self, surface):
        view_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        bar_rect = pygame.Rect(self.x, self.y, self.width, self.bar_height)

        # draw the background of the view
        if self.view_bg is not None:
            pygame.draw.rect(surface, self.view_bg, view_rect)

        if self.draggable:
            # draw the drag bar of the view
            pygame.draw.rect(surface, self.dragbar_bg, bar_rect)

            # draw the cross
            self._draw_cross(surface, self.bar_height, self.cross_line_width, self.cross_buffer, self.cross_color)

        # draw the cards
        if self.cards:
            self._draw_cards(surface)

        # draw the scrollbar
        self._draw_scrollbar(surface)
