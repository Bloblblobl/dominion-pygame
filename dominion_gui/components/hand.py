from dominion_gui.game_client import GameClient
from dominion_gui.components.card_view import CardView


class Hand(CardView):
    def on_click(self, ui_element):
        card = ui_element.container
        GameClient.instance.play_action_card(card.name)