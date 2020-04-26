import pygame


class CardStack(pygame.sprite.Group):
    def __init__(self, cards=None, pos=None):
        self.active_index = None
        self.pos = pos if pos is not None else (0, 0)
        super(CardStack, self).__init__()
        if cards is not None:
            self.add(cards)

    def scale(self, width, height):
        for sprite in self.sprites():
            sprite.scale(width, height)

    def add(self, *sprites):
        if self.active_index is None and sprites:
            self.active_index = 0
        super(CardStack, self).add(*sprites)

    def update(self, pressed_keys, *args):
        if self.active_index is not None:
            sprites = self.sprites()
            if pressed_keys[pygame.K_LEFT] and self.active_index > 0:
                self.active_index -= 1
            if pressed_keys[pygame.K_RIGHT] and self.active_index < len(sprites) - 1:
                self.active_index += 1
        super(CardStack, self).update(*([pressed_keys] + list(args)))

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        x, y = self.pos
        deltax = sprites[0].rect.width
        if sprites:
            if self.active_index > 0:
                left_spr = sprites[self.active_index - 1]
                left_spr.fade((0, 255), 100)
                left_rect = left_spr.rect
                left_rect.x = x
                left_rect.y = y
                self.spritedict[left_spr] = surface_blit(left_spr.image, left_spr.rect)

            x += deltax
            active_spr = sprites[self.active_index]
            active_spr.reset()
            active_rect = active_spr.rect
            active_rect.x = x
            active_rect.y = y
            x += deltax
            self.spritedict[active_spr] = surface_blit(active_spr.image, active_spr.rect)

            if self.active_index < len(sprites) - 1:
                right_spr = sprites[self.active_index + 1]
                right_spr.fade((255, 0), -100)
                right_rect = right_spr.rect
                right_rect.x = x
                right_rect.y = y
                x += deltax
                self.spritedict[right_spr] = surface_blit(right_spr.image, right_spr.rect)
