from kivy.app import App

from kivy.uix.boxlayout import BoxLayout
from scripts.ui.shadow import Shadow
from scripts.widgets.buttons import ShadowedButton
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen

from scripts.ui.popup import CEPopUp
from scripts.utils.manager import AppManager
from scripts.utils.eventmanager import EventManager
from scripts.ui.charts import BarPlot

from kivy.graphics import Color, Rectangle

class MainApp(App):

    def build(self):
        self.manager = AppManager()

        self.window = FloatLayout()
        self.current_screen: Screen = Screen()

        EventManager.set_trigger("AddPopUp", self.__add_popup)
        EventManager.set_trigger("RemovePopUp", self.__remove_popup)
        EventManager.set_trigger("ChangeScreen", self.__change_screen)

        self.manager.access_screen("TrainSelectionScreen")
        #self.window.add_widget(BarPlot({'a':30, 'b':50}))

        return self.window
    
    def __add_popup(self, popup: CEPopUp) -> None:
        self.window.add_widget(popup)
    
    def __remove_popup(self, popup: CEPopUp) -> None:
        try:
            self.window.remove_widget(popup)
        except:
            return
    
    def __change_screen(self, new_screen: Screen) -> None:
        self.window.remove_widget(self.current_screen)
        new_screen.on_pre_enter()
        self.window.add_widget(new_screen)
        self.current_screen = new_screen



if __name__ == '__main__':
    import os
    from scripts.utils.train import create_all_tables
    #os.remove('')
    create_all_tables()
    MainApp().run()
