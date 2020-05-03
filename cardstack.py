import pygame


class CardStack:
    def __init__(self, cards, screen_size, card_size):
        self.screen_width, self.screen_height = screen_size
        self.card_width, self.card_height = card_size

        self.cards = cards
        self.surface = pygame.Surface((self.screen_width, self.card_height))

        # determine the maximum number of cards that can appear on the screen at once
        self.max_visible = self.screen_width // self.card_width

        # set the initial set of cards in the stack to be rendered
        self.visible = list(range(min(len(self.cards), self.max_visible)))

        self.selected = None

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.selected is None:
                        self.selected = self.visible[0]
                    elif self.selected < self.visible[-1]:
                        self.selected += 1
                    elif self.visible[-1] < len(self.cards) - 1:
                        self.visible.pop(0)
                        self.visible.append(self.visible[-1] + 1)
                        self.selected += 1
                if event.key == pygame.K_LEFT:
                    if self.selected is None:
                        self.selected = self.visible[0]
                    elif self.selected > self.visible[0]:
                        self.selected -= 1
                    elif self.visible[0] > 0:
                        self.visible.pop(-1)
                        self.visible.insert(0, self.visible[0] - 1)
                        self.selected -= 1

    def draw(self, screen):
        self.surface.fill((0, 0, 0))
        x, y = 0, self.screen_height - self.card_height
        for n, i in enumerate(self.visible):
            selected = self.selected == i
            dest = (x + n * self.card_width, 0)
            self.cards[i].draw(surface=self.surface, dest=dest, selected=selected)
        screen.blit(self.surface, (x, y))


# class CardStack(pygame.sprite.Group):
#     def __init__(self, cards=None, pos=None):
#         self.active_index = None
#         self.pos = pos if pos is not None else (0, 0)
#         super(CardStack, self).__init__()
#         if cards is not None:
#             self.add(cards)
#
#     def scale(self, width, height):
#         for sprite in self.sprites():
#             sprite.scale(width, height)
#
#     def add(self, *sprites):
#         if self.active_index is None and sprites:
#             self.active_index = 0
#         super(CardStack, self).add(*sprites)
#
#     def update(self, pressed_keys, *args):
#         if self.active_index is not None:
#             sprites = self.sprites()
#             if pressed_keys[pygame.K_LEFT] and self.active_index > 0:
#                 self.active_index -= 1
#             if pressed_keys[pygame.K_RIGHT] and self.active_index < len(sprites) - 1:
#                 self.active_index += 1
#         super(CardStack, self).update(*([pressed_keys] + list(args)))
#
#     def draw(self, surface):
#         sprites = self.sprites()
#         surface_blit = surface.blit
#         x, y = self.pos
#         deltax = sprites[0].rect.width
#         if sprites:
#             if self.active_index > 0:
#                 left_spr = sprites[self.active_index - 1]
#                 left_spr.fade((0, 255), 100)
#                 left_rect = left_spr.rect
#                 left_rect.x = x
#                 left_rect.y = y
#                 self.spritedict[left_spr] = surface_blit(left_spr.image, left_spr.rect)
#
#             x += deltax
#             active_spr = sprites[self.active_index]
#             active_spr.reset()
#             active_rect = active_spr.rect
#             active_rect.x = x
#             active_rect.y = y
#             x += deltax
#             self.spritedict[active_spr] = surface_blit(active_spr.image, active_spr.rect)
#
#             if self.active_index < len(sprites) - 1:
#                 right_spr = sprites[self.active_index + 1]
#                 right_spr.fade((255, 0), -100)
#                 right_rect = right_spr.rect
#                 right_rect.x = x
#                 right_rect.y = y
#                 x += deltax
#                 self.spritedict[right_spr] = surface_blit(right_spr.image, right_spr.rect)
