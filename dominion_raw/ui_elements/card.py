import pygame


class Card:
    def __init__(self, name, image, back_image, card_size, border_thickness=2, border_color=(255, 0, 0, 200)):
        self.name = name
        self.image = image['small_image']
        self.gray_image = image['small_image_gray']
        self.zoom = image['zoom_image']
        self.back_image = back_image['small_image']
        self.width, self.height = card_size
        self.border_thickness = border_thickness
        self.border_color = border_color

    @property
    def total_width(self):
        return self.width + 2 * self.border_thickness

    @property
    def total_height(self):
        return self.height + 2 * self.border_thickness

    def update(self, *args, **kwargs):
        pass

    def draw(self, surface, dest, selected, face_up=True, disabled=False):
        border_rect = pygame.Rect(*dest, self.total_width, self.total_height)
        card_image = self.image if face_up else self.back_image
        if disabled:
            card_image = self.gray_image
        card_dest = (dest[0] + self.border_thickness, dest[1] + self.border_thickness)
        card_rect = pygame.Rect(*card_dest, self.width, self.height)
        if selected:
            pygame.draw.rect(surface, self.border_color, border_rect)

        surface.blit(card_image, card_rect)
        return border_rect


