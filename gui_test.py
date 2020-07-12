import pygame
import pygame_gui

from pygame_gui import UIManager
from pygame_gui.elements import UITextBox, UIPanel, UILabel

from pygame_raw.constants import screen_size, screen_width, screen_height

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode(screen_size)

background = pygame.Surface(screen_size)
background.fill(pygame.Color('#000000'))

manager = UIManager(screen_size)
manager.preload_fonts([dict(name='fira_code', point_size=14, style='bold')])

clock = pygame.time.Clock()

is_running = True

panel_size = panel_width, panel_height = 300, screen_height - 20
panel_pos = (screen_width - panel_width - 10, 10)
panel = UIPanel(relative_rect=pygame.Rect(panel_pos, panel_size),
                starting_layer_height=2,
                manager=manager)

# hello_button = UIButton(relative_rect=pygame.Rect((10, 10),(100, 50)),
#                         text='Hell0 W0rld',
#                         manager=manager,
#                         container=panel)

label_size = label_width, label_height = (100, 20)
label_pos = (0, 10)

label = UILabel(relative_rect=pygame.Rect(label_pos, label_size),
                text='Sidepanel',
                manager=manager,
                container=panel)

log_text = '<b>[Event]</b> <font color=#FF5CC9>WARNING!</font> Player 1 drew a card!<br>' \
           '<b>[Event]</b> Player 2 drew a card!<br>' * 20

log_size = (panel_width - 20, panel_height - 50)
log_pos = (7, 40)
log = UITextBox(relative_rect=pygame.Rect(log_pos, log_size),
                     html_text=log_text,
                     manager=manager,
                     container=panel)


while is_running:
    time_delta = clock.tick(60)/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()