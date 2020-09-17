from dominion_gui.ui_elements.html_textbox import HTMLTextBox


class MessageLog(HTMLTextBox):
    def __init__(self, layout_info, container, bg_color=None, padding=None):
        super().__init__('', layout_info, container, bg_color, padding)
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)
        self.html = '<br>'.join(self.messages)
