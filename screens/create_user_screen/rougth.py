from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from scripts.ui.popup import CEPopUp

from scripts.utils.train import add_user
from scripts.utils.eventmanager import EventManager
from scripts.utils.data_manager import DataManager

class RoughtNewUserPopUp(CEPopUp):
    data = {}
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__content = RoughtNewUserScreen()
        self.load_layout(self.__content)
    
    def on_pre_enter(self):
        self.__content.clean_text_fields()

    def on_pre_leave(self, *args):
        return
    
class RoughtNewUserScreen(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.size_hint_y = 0.5
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
        self.add_button = Button(text='ADD', on_press = self.create_user)

        self.layout.add_widget(self.exercice_name_field)
        self.layout.add_widget(self.add_button)
    
    def create_user(self, *args) -> None:
        if "" == (self.exercice_name_field.text.strip()):
            return
        add_user(self.exercice_name_field.text.strip())

        self.clean_text_fields()
        EventManager.trigger("NewUserAdded")
        EventManager.trigger("RemovePopUp", self.popup)
    
    def clean_text_fields(self, *args) -> None:
        self.exercice_name_field.text = ""

    