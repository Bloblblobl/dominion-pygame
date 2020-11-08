import copy
from collections import namedtuple

from typing import Callable

from dominion_gui.event_handler import EventHandler
from dominion_gui.event_manager import get_event_manager
from dominion_gui.ui_elements.button import Button
from dominion_gui.ui_elements.ui_element import UIElement
from layout_info.layout_info import LayoutInfo


Tab = namedtuple('Tab', ['content', 'button'])


class TabContainer(UIElement, EventHandler):
    def __init__(self,
                 layout_info: LayoutInfo,
                 container: UIElement,
                 tab_bar_height,
                 padding: LayoutInfo = None,
                 show_single_tab: bool = False):
        super().__init__(layout_info, container, padding)
        self.tabs = {}
        self.tab_buttons = []
        self.active_tab = ''
        self.tab_bar_li = LayoutInfo(left=0, right=0, top=0, height=tab_bar_height)
        self.active_tab_li = LayoutInfo(left=0, right=0, top=tab_bar_height, bottom=0)
        self.button_li = LayoutInfo(left=0, top=0, width=0, height=self.tab_bar_li.height)
        self.show_single_tab = show_single_tab

    def select_tab(self, name: str):
        if name == self.active_tab:
            return
        if name not in self.tabs:
            raise RuntimeError('No such tab ' + name)
        self.tabs[self.active_tab].content.visible = False
        self.active_tab = name
        self.tabs[name].content.visible = True
        self.layout(only_if_changed=False)

    def add_tab(self, name: str, tab_button_width: int, tab_factory: Callable, **kwargs):
        tab = tab_factory(layout_info=self.active_tab_li, container=self, **kwargs)
        if not self.active_tab:
            self.active_tab = name
        else:
            tab.visible = False

        self.button_li.width = tab_button_width
        tab_button = Button(name, copy.deepcopy(self.button_li), self)
        self.tabs[name] = Tab(tab, tab_button)
        get_event_manager().subscribe(tab_button, 'on_ui_button_press', self)
        self.tab_buttons.append(tab_button)
        self.button_li.left += self.button_li.width

        if len(self.tab_buttons) == 1:
            tab_button.visible = self.show_single_tab
        else:
            for b in self.tab_buttons:
                b.visible = True

    def remove_tab(self, name: str, new_active: str = ''):
        if name == new_active:
            raise RuntimeError('New active can\'t be the removed tab ' + name)
        if name not in self.tabs:
            raise RuntimeError('No such tab ' + new_active)
        if name == self.active_tab and new_active not in self.tabs:
            raise RuntimeError('No such tab ' + new_active)
        if name != self.active_tab and new_active in self.tabs:
            raise RuntimeError('Removed tab is not active, can\'t select ' + new_active)

        if name == self.active_tab:
            self.select_tab(new_active)
        get_event_manager().unsubscribe(self.tabs[name].button, 'on_ui_button_press')
        self.tabs[name].content.kill()
        self.tabs[name].button.kill()
        del self.tabs[name]

        self.tab_buttons = [b for b in self.tab_buttons if b.text != name]
        left = 0
        for b in self.tab_buttons:
            b.layout_info.left = left
            left += b.layout_info.width

        if len(self.tab_buttons) == 1:
            self.tab_buttons[0].visible = self.show_single_tab

        self.layout(only_if_changed=False)

    def on_ui_button_press(self, *, ui_element):
        self.select_tab(ui_element.text)
        if ui_element.text == 'red' and 'blue' in self.tabs:
            self.remove_tab('blue')
