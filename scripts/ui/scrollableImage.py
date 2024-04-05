from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

class ScrollableImage(ScrollView):
    def __init__ (self, source: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.source = source
        self.image = Widget(size_hint_x = None)
        self.image_ratio = Image(source=source).image_ratio
        self.add_widget(self.image)
        self.image.bind(size = self.resize_image)
                        
    def resize_image(self, *args):
        self.image_ratio = Image(source=self.source).image_ratio
        self.image.width = self.height * self.image_ratio
        with self.image.canvas:
            self.image.canvas.clear()
            Color(rgb=(1,1,1))
            Rectangle(
                size = self.image.size,
                pos = self.image.pos,
                source = self.source,
            )
