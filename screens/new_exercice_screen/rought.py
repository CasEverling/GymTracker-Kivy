print("Hello world!")

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from scripts.ui.popup import CEPopUp

from scripts.utils.train import add_exercice, add_exercices_to_train, get_train
from scripts.utils.data_manager import DataManager
from scripts.utils.eventmanager import EventManager

class RoughtNewExercicePopUp(CEPopUp):
    data = {}
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__content = RoughtNewExerciceScreen()
        self.load_layout(self.__content)
    
    def on_pre_enter(self):
        self.__content.clean_text_fields()

    def on_pre_leave(self, *args):
        return
    
class RoughtNewExerciceScreen(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.size_hint_y = 0.9
        self.built = False
        self.layout = BoxLayout(orientation ='vertical') 
        self.add_widget(self.layout)
        self.build()
    
    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        if not self.built:
            self.build()
            self.built = True
        else:
            self.clean_text_fields()

    def build(self) -> None:
        self.layout.clear_widgets()

        self.exercice_name_field = TextInput()
        self.exercice_description_field = TextInput()
        self.exercice_metric_field = TextInput()
        self.add_button = Button(text='ADD', on_press = self.add_exercice)

        self.layout.add_widget(self.exercice_name_field)
        self.layout.add_widget(self.exercice_description_field)
        self.layout.add_widget(self.exercice_metric_field)
        self.layout.add_widget(self.add_button)
    
    def add_exercice(self, *args) -> None:
        if "" in (self.exercice_name_field.text.strip(), self.exercice_description_field.text.strip(), self.exercice_metric_field.text.strip()):
            return
        exercice_id = add_exercice(self.exercice_name_field.text.strip(), self.exercice_description_field.text.strip(), self.exercice_metric_field.text.strip())
        add_exercices_to_train(DataManager.current_train.train_id, [exercice_id])
        DataManager.current_train = get_train(DataManager.current_train.train_id)
        self.clean_text_fields()
        EventManager.trigger("TrainUpdated")
        EventManager.trigger("RemovePopUp", self.popup)

    
    def clean_text_fields(self, *args) -> None:
        self.exercice_name_field.text = self.exercice_description_field.text = self.exercice_metric_field.text = ""
