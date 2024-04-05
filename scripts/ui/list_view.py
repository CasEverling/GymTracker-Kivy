print("Hello World!")

from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

from scripts.ui.line import Line

from typing import List, Generic

from scripts.utils.eventmanager import EventManager


T = type[Generic]
class ListView(ScrollView):
    def __init__(self, content: List[T], callbak: str = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.callback = callbak
        self.box = BoxLayout(size_hint_y = None, orientation = 'vertical', padding = dp(10), spacing = dp(15))
        self.box.bind(minimum_height = self.box.setter("height"))

        self.is_first = True
        for item in content:
            self.add_item(item)

        self.add_widget(self.box)
        
    def add_item(self, content: T, **kwargs) -> None:
        if self.is_first:
            self.box.add_widget(Line())
            self.is_first = False
        button = Button(
            text = str(content), 
            on_press = self.click,
            size_hint_y = None,
            height = dp(60),
            )
        button.content = content
        self.box.add_widget(button)

    def click(self, button, *args) -> None:
        EventManager.trigger(self.callback, button.content)


    