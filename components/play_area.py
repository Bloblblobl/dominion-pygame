from constants import card_spacing, screen_height

from ui_elements.cardview import CardView

visible_cards = 5


class PlayArea(CardView):
    def __init__(self, cards, on_card_selected_callback):
        super().__init__(cards,
                         visible_cards,
                         draggable=False,
                         spacing=card_spacing,
                         on_card_selected=on_card_selected_callback)
        self.x = 0
        self.y = screen_height - 2 * self.height
        self.view_bg = None