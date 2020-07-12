from client import object_model
from dominion_raw.constants import card_spacing
from dominion_raw.ui_elements.single_card_stack import SingleCardStack
import math
import pygame

stacks_per_row = 8


class Shop:
    def __init__(self, card_counts, game_client: object_model.GameClient, pos=(0, 0)):
        self.x, self.y = pos
        self.spacing = card_spacing
        self.stacks = []
        self.width = 0
        self.height = 0
        self.game_client = game_client
        self.selected_card = None
        self.initialize_stacks(card_counts)
        self.background_color = None

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def _on_stack_click(self, stack):
        self.game_client.buy(stack.card.name)

    def initialize_stacks(self, card_counts):
        self.stacks = []
        for i, card_count in enumerate(card_counts):
            stack = SingleCardStack(*card_count, on_click=self._on_stack_click)
            stack.x = self.x + (stack.max_width + self.spacing) * (i % stacks_per_row)
            stack.y = self.y + (stack.max_height + self.spacing) * (i // stacks_per_row)
            stack.update_rect()
            self.stacks.append(stack)
        num_rows = math.ceil(len(self.stacks) / stacks_per_row)
        self.width = (self.stacks[0].max_width + self.spacing) * stacks_per_row - self.spacing
        self.height = (self.stacks[0].max_height + self.spacing) * num_rows - self.spacing

    def draw(self, surface, disabled=False):
        if self.background_color is not None:
            pygame.draw.rect(surface, self.background_color, self.rect)
        for stack in self.stacks:
            stack.draw(surface, disabled)

    def update(self):
        for stack in self.stacks:
            if stack.state == 'hover':
                self.selected_card = stack.card
                return
        self.selected_card = None

    def handle_mouse_event(self, event_type, pos):
        for stack in self.stacks:
            stack.handle_mouse_event(event_type, pos)
