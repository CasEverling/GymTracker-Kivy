from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from typing import List, Generic, Generator

from scripts.utils.eventmanager import EventManager

T = type[Generic]

class ScrollButtonChain(ScrollView):

    def __init__(self, single_selection = False, data_objects: List[T] = [], option_selection_event = None, add_option_event = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.option_selection_event = option_selection_event
        self.single_selection = single_selection
        self.do_scroll_x = True
        self.size_hint_y = None
        self.box = BoxLayout(spacing = dp(15), padding = dp(15), size_hint = (None, None))
        self.box.bind(minimum_size = self.box.setter('size'), height = self.setter('height'))
        self.box.add_widget(Button(on_press = self.add_button, text = '+', size_hint = (None, None), size = (dp(60) ,dp(60))))
        self.buttons: List[ToggleButton] = []
        EventManager.set_trigger("AddUsers", self.add_users)

        self.add_widget(self.box)
        self.add_users(data_objects)

    def add_users(self, data_objects: List[T]) -> None:
        for data_object in data_objects:
            toggle_button = ToggleButton(on_press = self.click, text = str(data_object), size_hint = (None, None), size = (dp(60), dp(60)))
            toggle_button.content = data_object
            self.buttons.append(toggle_button)
            self.box.add_widget(toggle_button, 1)
    
    def get_selected_buttons(self) -> Generator:
        for button in self.buttons:
            if button.state == "up":
                yield button
    
    def add_button(self, *args) -> None:
        EventManager.trigger("OpenPopUp", "CreateUserPopUp")
    
    def click(self, pressed_button, *args):
        if (self.single_selection) and (pressed_button.state == 'down'):
            for button in self.buttons:
                if (button.state == 'down') and (button != pressed_button):
                    button.state = 'normal'
        self.option_selection_event(pressed_button)
