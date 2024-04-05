print("Hello World!")

import threading
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp

from scripts.ui.toggle_button_chain import ScrollButtonChain
from scripts.ui.list_view import ListView
from scripts.utils.data_manager import DataManager
from scripts.utils.eventmanager import EventManager

from scripts.utils.train import get_section, edit_section_info, get_exercice_history, get_exercice, create_section
from scripts.utils.charts import build_bar_chart 

class RoughtTrainSectionScreen(Screen):
    def __init__ (self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.build()
        self.load()

    def build(self):
        self.layout = BoxLayout(orientation = 'vertical')
        self.current_users = ScrollButtonChain(True, option_selection_event=self.select_user)
        box = BoxLayout(orientation = 'vertical')
        bottom_bar = BoxLayout(size_hint_y = None, height = dp(60))

        self.previous_button: Button = Button(text = '', on_press = self.previous)
        self.next_button: Button = Button(text = 'Next ->', on_press = self.next)
        

        bottom_bar.add_widget(self.previous_button)
        bottom_bar.add_widget(self.next_button)


        box.add_widget(ExerciceController())
        box.add_widget(bottom_bar)

        self.layout.add_widget(self.current_users)
        self.layout.add_widget(box)
        self.add_widget(self.layout)
        self.built = True
        

    def load(self, *args) -> None:
        self.load_users()

    def next(self, *args):
        self.previous_button.text = '<- Previous'
        difference: int = len(DataManager.current_train.exercices) - DataManager.current_exercice_index - 1
        print(difference)
        if difference:
            DataManager.current_exercice_index += 1
            EventManager.trigger("ExerciceChanged")
            if difference == 1:
                self.next_button.text = 'Finish'

    def previous(self, *args):
        print(DataManager.current_exercice_index)
        self.next_button.text = 'Next ->'
        if DataManager.current_exercice_index:
            DataManager.current_exercice_index -= 1
            EventManager.trigger("ExerciceChanged")
            if not DataManager.current_exercice_index:
                self.previous_button.text = ''
    
    def on_leave(self, *args) -> None:
        DataManager.current_exercice_index = 0
        DataManager.current_section_ids = []

    def on_pre_enter(self, *args) -> None:
        DataManager.current_exercice_index = 0
        DataManager.current_section_ids = []
        for user in DataManager.current_users:
            DataManager.current_section_ids.append(create_section(user.user_id, DataManager.current_train.train_id))
        self.load()
        EventManager.trigger("ExerciceChanged")
    
    def load_users(self, *args) -> None:
        self.current_users.box.clear_widgets()
        self.current_users.buttons = []
        self.current_users.add_users(DataManager.current_users)
        self.current_users.children[0].children[DataManager.current_user].state = 'down'

    def select_user(self, button, *args) -> None:
        DataManager.current_user = DataManager.current_users.index(button.content)
        EventManager.trigger("ExerciceChanged")        

    
class ExerciceController(BoxLayout):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = self.spacing = dp(15)
        EventManager.set_trigger("ExerciceChanged", self.load_info)
        self.build()
        self.load_info()

    def build(self) -> None:
        
        self.title = Button(size_hint_y = None, height = dp(60))
        self.add_widget(self.title)
        #AddOpenChartButton
        self.add_widget(Button(text='Chart View', on_press = self.open_chart, size_hint_y = None, height = dp(60)))
        #AddPastTrainIndo
        self.history_list_view = ListView([])
        self.add_widget(self.history_list_view)
        #AddTextInput (numbers - only)
        self.text=TextInput(size_hint_y = None, height = dp(60))
        self.add_widget(self.text)
        self.text.bind(text=self.update_value)



    def load_info(self) -> None:
        self.title.text = get_exercice(DataManager.current_train.exercices[DataManager.current_exercice_index]).name
        self.exercice_history = get_exercice_history(
            user_id= DataManager.current_users[DataManager.current_user].user_id,
            exercice_id= DataManager.current_exercice_index
        )
        self.exercice = get_exercice(DataManager.current_train.exercices[DataManager.current_exercice_index])

        data = {(i+1):value for i, value in enumerate(self.exercice_history)}
        if data == {}:
            return

        DataManager.train_history = data
        #self.open_chart()

    def open_chart(self, *args) -> None:
        EventManager.trigger("OpenPopUp", "ChartPopUp")
        EventManager.trigger('ChartUpdated')

    def update_value(self, field, text: str) -> None:
        if len(text) == 0:
            field.text = '0'
            return
        if text[-1:].isdigit() or text[-1] == '.':
            edit_section_info(
                DataManager.current_section_ids[DataManager.current_user],
                DataManager.current_train.exercices[DataManager.current_exercice_index],
                float(text)
            )
        else:
            field.text = text[:-1]
        

