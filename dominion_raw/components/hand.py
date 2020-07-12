from dominion_raw.constants import card_spacing, screen_height

from dominion_raw.ui_elements.card_view import CardView

visible_cards = 5


class Hand(CardView):
    def __init__(self, cards, on_card_selected_callback):
        super().__init__(cards,
                         visible_cards,
                         draggable=False,
                         spacing=card_spacing,
                         on_card_selected=on_card_selected_callback)
        self.x = 0
        self.y = screen_height - self.height
