from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.layout import Layout
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button

from scripts.utils.eventmanager import EventManager

    
class CEPopUp(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(
            size = self._draw_background,
            pos = self._draw_background
            )

    def _draw_background(self, *args):
        with self.canvas.before:
            self.canvas.before.clear()
            Color(rgba = (0,0,1, 0.3))
            Rectangle(
                pos = self.pos,
                size = self.size,
            )
    def on_touch_down(self, touch):
        if (
            (touch.x < self.children[0].x) or
            (touch.x > self.children[0].x + self.children[0].width) or
            (touch.y < self.children[0].y) or
            (touch.y > self.children[0].y + self.children[0].height)
            ):
            self.close()
            return True
        return super().on_touch_down(touch)
    
    def close(self, *args):
        EventManager.trigger("RemovePopUp", popup = self)

    def load_layout(self, layout: Layout) -> None:
        self.clear_widgets()
        layout.pos_hint = {'center_x':0.5, 'center_y':0.5}
        layout.size_hint_x = 0.8
        layout.bind(minimum_height = layout.setter("height"))
        layout.popup = self
        self.add_widget(layout)