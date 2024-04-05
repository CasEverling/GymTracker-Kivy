from scripts.ui.shadow import Shadow

from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle

class ShadowedButton(Button):
    def __init__(self, shadow: Shadow, **kwargs):
        super().__init__(**kwargs)
        self.shadow: Shadow = shadow
    
    def on_press(self):
        self.shadow.draw_shadow(self)


    