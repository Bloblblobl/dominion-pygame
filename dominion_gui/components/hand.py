from dominion_gui import game_client
from dominion_gui.components.card_view import CardView


class Hand(CardView):
    def on_click(self, ui_element):
        card = ui_element.container
        game_client.get_instance().play_action_card(card.name)