
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp

class _BarPlot:
    def __init__(
            self,
            data,
            title = '',
            x_label = '',
            y_label = '',
            size = None,
            title_font_size = 12,
            label_font_size = 10,
            show_values = False,
            show_values_on_bars = False,
            grid = False,
            background_color = (1,1,1,1),
            title_color = (0,0,0,1),
            labels_color = (0,0,0,1),
            grid_color = (0,0,0,0.5),
            bar_color = (0,0,0,1),
            values_color = (0,0,0,1),
            bar_style = 0,
            ) -> None:
                
        self.__data = data
        self.__title = title
        self.__x_label = x_label
        self.__y_label = y_label

        self.__size = size

        self.__grid = grid

        self.__colors = {
            'bg': background_color,
            'title': title_color,
            'label': labels_color,
            'values': values_color,
            'grid': grid_color,
        }

        self.__value_on_chart = show_values_on_bars

        self.__built = False
        self.__chart = Widget()
        self.__build()
        

    def __build(self) -> None:
        self.add_widget()

    def __draw(self) -> None:
        self.__chart.canvas.clear()
        with self.__chart.canvas.before:
            # Draw Background
            Color(rgba = self.__)

            # Draw Grid
            if self.__grid:
                # Draw Grid
                if self.__values_on_grid:
                    # Draw Lables
                    pass


            for label, value in self.__data.items():
                if self.__value_on_chart:
                    # Draw value
                    pass

                # Select Bar Style
                # Draw Bar
            
            # Draw Title
            # Draw Label X
            # Draw Label Y
            
            


    def load_data(self):
        pass

    def export():
        pass

class BarPlot(BoxLayout):
    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)

        self.max = max(data.values())
        self.spacing = self.padding = (dp(15))
        self.size_hint_x = None
        self.bind(minimum_width = self.setter('width'))
        self.load_data(data)
        
    
    def load_data(self, data):
        self.clear_widgets()
        for key, value in data.items():
            try:
                height = value/self.max
            except ZeroDivisionError:
                height = 0
            print(height)

            box = BoxLayout(orientation = 'vertical', size_hint_x = None, width = dp(60))
            box.add_widget(Widget(size_hint_y = 1-height))
            box.add_widget(Button(
                text = str(value),
                size_hint_y = height,
                on_press = self.print,
            ))
            self.add_widget(box)
    
    def print(self, button, *args):
        print(button.text, button.size_hint, button.width/dp(1))
        print(self.parent.size_hint, self.parent.size, len(self.parent.children))