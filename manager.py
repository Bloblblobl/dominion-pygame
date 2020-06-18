from components.discard_pile import DiscardPile
from components.play_area import PlayArea
from client.client import (
    Client,
    ClientEventHandler)

from components.hand import Hand

class Manager(ClientEventHandler):
    def __init__(self,
                 #client: Client,
                 play_area,
                 discard_pile):
        #self.client = client
        self.play_area = play_area
        self.discard_pile = discard_pile

    def on_card_selected(self, card_view, card):
        """
        TEMPORRY!!!!!!

        Need to play action card and NOT mess with hand and play area

        """

        if isinstance(card_view, Hand):
            h = card_view
            self.play_area.cards.insert(0, card)
            del h.cards[h.selected_index + h.start_index]
            if h.start_index > 0:
                h.start_index -= 1
            if len(h.cards) < h.num_cards_visible:
                del h.card_rects[-1]
        elif isinstance(card_view, PlayArea):
            play_area = card_view
            self.discard_pile.cards.insert(0, play_area.selected_card)
            del play_area.cards[play_area.selected_index + play_area.start_index]
            if play_area.start_index > 0:
                play_area.start_index -= 1
            if len(play_area.cards) < play_area.num_cards_visible:
                del play_area.card_rects[-1]

    # ClientEventHandler methods
    def on_play(self):
        pass

    def on_respond(self):
        pass
