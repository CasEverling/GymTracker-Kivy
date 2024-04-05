print('Hello World!')

from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.graphics import Color, Rectangle

class Line(Widget):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(1)
        self.bind(pos = self.draw, size = self.draw)

    def draw(self, *args):
        with self.canvas.before:
            self.canvas.before.clear()
            Color(rgb=(0,0,0))
            Rectangle(
                size = self.size,
                pos = self.pos
            )
