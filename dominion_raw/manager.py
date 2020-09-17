from .components.deck import Deck
from .components.play_area import PlayArea
from client.client import (
    Client,
    ClientEventHandler)

from .components.hand import Hand


class Manager(ClientEventHandler):
    def __init__(self,
                 client: Client,
                 hand,
                 play_area,
                 discard_pile):
        self.client = client
        self.hand = hand
        self.play_area = play_area
        self.discard_pile = discard_pile

    def on_card_selected(self, card_view, card):
        """
        TEMPORARY!!!!!!

        Need to play action card and NOT mess with hand and play area

        """

        if isinstance(card_view, Hand):
            self.client.play_action_card(card.name)
        elif isinstance(card_view, PlayArea):
            play_area = card_view
            self.discard_pile.piles.insert(0, play_area.selected_card)
            del play_area.cards[play_area.selected_index + play_area.start_index]
            if play_area.start_index > 0:
                play_area.start_index -= 1
            if len(play_area.cards) < play_area.num_cards_visible:
                del play_area.card_rects[-1]

    def on_click(self, card_stack):
        if isinstance(card_stack, Deck):
            deck = card_stack
            if deck.cards:
                self.hand.piles.append(deck.cards[-1])
                del deck.cards[-1]

    # ClientEventHandler methods
    def on_play(self):
        pass

    def on_respond(self):
        pass
