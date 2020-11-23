import functools

import pygame

from dominion_gui.components.default import get_default_layout
from dominion_gui.components.response import Response
from dominion_gui.components.stack import Stack
from dominion_gui.event_handler import EventHandler
from dominion_gui.components.card_view import CardView
from dominion_gui.components.message_log import MessageLog
from dominion_gui.components.shop import Shop
from dominion_gui.constants import background_color, screen_size, Colors, GREEN, BLUE, RED
from dominion_gui.ui_elements.button import Button
from dominion_gui.ui_elements.enums import Position, Orientation
from dominion_gui.ui_elements.horizontal_scroll_container import HorizontalScrollContainer
from dominion_gui.ui_elements.panel import Panel
from dominion_gui.ui_elements.tab_container import TabContainer
from dominion_gui.ui_elements.top_level_window import TopLevelWindow
from layout_info.layout_info import LayoutInfo

li_all_10 = LayoutInfo(left=10, right=10, top=10, bottom=10)


class UI(EventHandler):
    def __init__(self):
        self.background = pygame.Surface(screen_size)
        self.background.fill(background_color)
        self.window = TopLevelWindow(screen_size)

        top_level_container = Panel(li_all_10, self.window, Colors.BORDER)

        shop_play_container_li = LayoutInfo(left=20, right=30.25, top=20, bottom=10.3)
        shop_play_container = Panel(shop_play_container_li, top_level_container, Colors.STORE)
        shop_li = LayoutInfo(left=0, right=0, top=0, height=0.5)
        self.shop = Shop(shop_li, shop_play_container)

        play_area_li = LayoutInfo(left=0, right=0, bottom=0, height=0.5)
        self.play_tabs = TabContainer(play_area_li, shop_play_container, tab_bar_height=30)
        self.play_tabs.add_tab(name='Play Area',
                               tab_button_width=100,
                               tab_factory=HorizontalScrollContainer,
                               scrollable_class=CardView,
                               button_thickness=0.035)
        self.play_tabs.add_tab(name='Response',
                               tab_button_width=100,
                               tab_factory=Response,
                               prompt_text='This is a test prompt',
                               card_names=['village', 'market'],
                               button_names=['Yes', 'No'])
        self.play_area = self.play_tabs.tabs['Play Area'].content

        hand_container_li = LayoutInfo(left=20, right=30.25, top=0.7, bottom=20)
        hand_container = Panel(hand_container_li, top_level_container, Colors.HAND)
        self.hand = HorizontalScrollContainer(li_all_10, hand_container, CardView, 0.035)

        side_panel_container_li = LayoutInfo(right=20, top=20, bottom=20, width=0.25)
        side_panel_container = Panel(side_panel_container_li, top_level_container, Colors.SIDE_PANEL)
        self.build_side_panel(side_panel_container)

    def build_side_panel(self, container):
        message_log_li = LayoutInfo(left=0, right=0, top=0, height=0.8)
        self.message_log = MessageLog(message_log_li, container, padding=li_all_10)

        top_button_li = LayoutInfo(left=0, right=0, top=0.8, height=0.1)
        top_button_padding = LayoutInfo(left=10, right=10, top=0, bottom=10)
        top_button_text = 'Start Game'
        self.top_button = Button(text=top_button_text,
                                 layout_info=top_button_li,
                                 container=container,
                                 padding=top_button_padding,
                                 corner_radius_ratio=0.2)

        bottom_button_li = LayoutInfo(left=0, right=0, top=0.9, height=0.1)
        bottom_button_padding = LayoutInfo(left=10, right=10, top=0, bottom=10)
        bottom_button = 'End Turn'
        self.bottom_button = Button(text=bottom_button,
                                    layout_info=bottom_button_li,
                                    container=container,
                                    padding=bottom_button_padding,
                                    corner_radius_ratio=0.2)
