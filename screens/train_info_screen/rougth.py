from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.metrics import dp

from scripts.ui.toggle_button_chain import ScrollButtonChain
from scripts.ui.list_view import ListView

from scripts.utils.data_manager import DataManager
from scripts.utils.eventmanager import EventManager

from scripts.utils.train import get_exercice

class TrainInfoScreen(Screen):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.built = False
        self.build()
        self.load_data()
        EventManager.set_trigger("TrainUpdated", self.load_exercices)

    def on_pre_enter(self, *args):
        self.load_data()
        
    def build(self):
        self.layout = BoxLayout(orientation = 'vertical')
        self.title = Button(text=DataManager.current_train.title, size_hint_y = None, height = dp(60))
        box = BoxLayout(orientation = 'vertical')
        bottom_bar = FloatLayout(size_hint_y = None, height = dp(60))
        bottom_bar.add_widget(Button(text = 'Start Train', on_press = self.start_section))
        bottom_bar.add_widget(Button(
            text = '+',
            size_hint = (None, None),
            size = 2*(dp(60),),
            pos_hint = {'right':0.95, 'top': 1.5},
            on_press = self.click_on_add_exercice,
        ))
        self.exercices = ListView([])
        box.add_widget(self.exercices)
        box.add_widget(bottom_bar)

        self.layout.add_widget(self.title)
        self.layout.add_widget(box)
        self.add_widget(self.layout)
        self.built = True

    def load_data(self):
        if not self.built:
            self.build()
        self.title = DataManager.current_train.title
        self.load_exercices()
    
    def load_exercices(self):
        self.exercices.box.clear_widgets()
        for exercice_id in DataManager.current_train.exercices:
            self.exercices.add_item(get_exercice(exercice_id))

    def click_on_add_exercice(self, *args):
        EventManager.trigger("OpenPopUp", "NewExercicePopUp")
    
    def start_section(self, *args):
        EventManager.trigger("OpenScreen", "TraiSectionScreen")
        

    

        
        
