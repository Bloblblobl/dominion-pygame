from constants import card_spacing
from ui_elements.single_card_stack import SingleCardStack

stack_count = 10
stacks_per_row = 8


class Shop:
    def __init__(self, cards, pos=(0, 0)):
        self.x, self.y = pos
        self.spacing = card_spacing
        self.stacks = []
        for i, card in enumerate(cards):
            stack = SingleCardStack(card, stack_count)
            stack.x = self.x + (stack.max_width + self.spacing) * (i % stacks_per_row)
            stack.y = self.y + (stack.max_height + self.spacing) * (i // stacks_per_row)
            self.stacks.append(stack)

    def draw(self, surface):
        for stack in self.stacks:
            stack.draw(surface)

    def update(self):
        pass
