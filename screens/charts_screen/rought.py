from kivy.uix.layout import Layout
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from scripts.utils.charts import build_bar_chart
from scripts.ui.scrollableImage import ScrollableImage
from kivy.uix.scrollview import ScrollView

from scripts.ui.popup import CEPopUp
from scripts.ui.charts import BarPlot
from scripts.utils.data_manager import DataManager
from scripts.utils.eventmanager import EventManager

class RoughChartPopUp(CEPopUp):
    data = {}
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__content = RoughtChartScreen()
        self.load_layout(self.__content)
    
    def on_pre_enter(self):
        self.__content.build_chart(self.data)
        self.__content.show_chart()

    def on_pre_leave(self, *args):
        return
    
class RoughtChartScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = 0.8
        scroll = ScrollView(do_scroll_x = True, do_scroll_y = False)
        self.__chart = BarPlot({0:0})
        scroll.add_widget(self.__chart)
        self.add_widget(scroll)
        EventManager.set_trigger("ChartUpdated", self.show_chart)
    
    def build_chart(self, data) -> None:
        build_bar_chart(data,"","","",(7.5,5))

    def show_chart(self) -> None:
        self.__chart.load_data(DataManager.train_history)
