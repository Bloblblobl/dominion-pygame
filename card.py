import pygame
import math

from util import load_image


class Card:
    def __init__(self, name, image, card_size, border_size=2, border_color=(255, 0, 0, 200)):
        self.name = name
        self.image = image['small_image']
        self.zoom = image['zoom_image']
        # for now this counterintuitively includes the border size
        self.width, self.height = card_size
        self.border_size = border_size
        self.border_color = border_color

    def update(self, *args, **kwargs):
        pass

    def draw(self, surface, dest, selected):
        dest_rect = pygame.Rect(*dest, self.width, self.height)
        if selected:
            pygame.draw.rect(surface, self.border_color, dest_rect)
        dest = (dest[0] + self.border_size, dest[1] + self.border_size)
        surface.blit(self.image, dest)
        return dest_rect


# class Card(pygame.sprite.Sprite):
#     def __init__(self, name):
#         super(Card, self).__init__()
#         self.image = load_image(name)
#         self.rect = self.image.get_rect()
#
#     def reset(self):
#         self.image.set_alpha(255)
#         self.image = self.image.convert()
#         self.rect = self.image.get_rect()
#
#     def scale(self, width, height):
#         self.image = pygame.transform.scale(self.image, (width, height))
#
#     def update(self, *args):
#         pass
#
#     def fade(self, fade_range=(255, 0), offset=0):
#         alpha_left, alpha_right = fade_range
#         alpha = alpha_left
#
#         self.image.set_alpha(alpha_left)
#         alpha_image = self.image.convert_alpha()
#         width = alpha_image.get_width()
#         height = alpha_image.get_height()
#
#         alpha_diff = alpha_left - alpha_right
#         alpha_delta = alpha_diff / width
#
#         if offset < 0:
#             alpha += offset * alpha_delta
#             alpha = min(max(alpha, 0), 255)
#             offset = 0
#
#         for x in range(offset, width):
#             for y in range(height):
#                 pixel = alpha_image.get_at((x, y))
#                 pixel.a = math.floor(alpha)
#                 alpha_image.set_at((x, y), pixel)
#             alpha -= alpha_delta
#             alpha = min(max(alpha, 0), 255)
#
#         self.image = alpha_image
