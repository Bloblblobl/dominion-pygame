import pygame
from pathology.path import Path

screen_size = screen_width, screen_height = 1080, 700
min_screen_size = min_screen_width, min_screen_height = 640, 400
background_color = '#000000'
preloaded_fonts = [dict(name='fira_code', html_size=2, style='regular'),
                   dict(name='fira_code', point_size=12, style='regular')]

RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(255, 255, 0)
GRAY = pygame.Color(200, 200, 200)
DARK_GRAY = pygame.Color(100, 100, 100)

theme_path = str((Path.script_dir() / 'theme.json').resolve())