from constants import card_spacing
from ui_elements.single_card_stack import SingleCardStack
import math

stacks_per_row = 8


class Shop:
    def __init__(self, card_counts, pos=(0, 0)):
        self.x, self.y = pos
        self.spacing = card_spacing
        self.stacks = []
        self.width = 0
        self.height = 0
        self.initialize_stacks(card_counts)

    def initialize_stacks(self, card_counts):
        self.stacks = []
        for i, card_count in enumerate(card_counts):
            stack = SingleCardStack(*card_count)
            stack.x = self.x + (stack.max_width + self.spacing) * (i % stacks_per_row)
            stack.y = self.y + (stack.max_height + self.spacing) * (i // stacks_per_row)
            self.stacks.append(stack)
        num_rows = math.ceil(len(self.stacks) / stacks_per_row)
        self.width = (self.stacks[0].max_width + self.spacing) * stacks_per_row - self.spacing
        self.height = (self.stacks[0].max_height + self.spacing) * num_rows - self.spacing

    def draw(self, surface):
        for stack in self.stacks:
            stack.draw(surface)

    def update(self):
        pass
