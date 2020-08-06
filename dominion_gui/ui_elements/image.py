import pygame
from pygame_gui.elements import UIImage

from dominion_gui.ui_elements.ui_element import UIElement


class Image(UIElement):
    def __init__(self, layout_info, container, image_path, padding=None):
        super().__init__(layout_info, container, padding)
        image_surface = pygame.image.load(image_path).convert_alpha()
        self.element = UIImage(relative_rect=self.bounds,
                               image_surface=image_surface,
                               manager=self.manager)

