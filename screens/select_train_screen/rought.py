from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

from kivy.metrics import dp

from scripts.ui.toggle_button_chain import ScrollButtonChain
from scripts.ui.list_view import ListView

from scripts.utils.data_manager import DataManager
from scripts.utils.eventmanager import EventManager

from scripts.utils.train import get_all_users, get_trains
from scripts.data_abstractions.user import User

class SelectTrainScreen(Screen):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.built = False
        self.build()
        self.load_data()

        EventManager.set_trigger("NewUserAdded", self.load_users)
        EventManager.set_trigger("NewTrainAssigned", self.load_trains)
        EventManager.set_trigger("SelectTrain", self.click_on_train)
    
    def build(self):
        self.layout = BoxLayout(orientation = 'vertical')
        self.current_users = ScrollButtonChain(
            option_selection_event= self.click_on_user,
            )
        box = BoxLayout(orientation = 'vertical')
        bottom_bar = FloatLayout(size_hint_y = None, height = dp(60))
        bottom_bar.add_widget(Button(
            text = '+',
            size_hint = (None, None),
            size = 2*(dp(60),),
            pos_hint = {'right':0.95, 'top': 1.5},
            on_press = self.click_on_add_train,
        ))
        self.exercices = ListView([], "SelectTrain")
        box.add_widget(self.exercices)
        box.add_widget(bottom_bar)

        self.layout.add_widget(self.current_users)
        self.layout.add_widget(box)
        self.add_widget(self.layout)
        self.built = True

    def load_data(self):
        if not self.built:
            self.build()
        self.load_users()
        self.load_trains()

    def load_users(self):
        self.current_users.box.clear_widgets(self.current_users.buttons)
        self.current_users.buttons = []
        self.current_users.add_users(get_all_users())
        DataManager.current_users = []
        DataManager.current_user = 0
    
    def load_trains(self):
        self.exercices.box.clear_widgets()
        for train in get_trains([user.user_id for user in DataManager.current_users]):
            self.exercices.add_item(train)

    def click_on_user(self, button, *args) -> None:
        if button.state == 'normal':
            DataManager.current_users.remove(button.content)
        else:
            DataManager.current_users.append(button.content)
        self.load_trains()
    
    def click_on_add_train(self, *args) -> None:
        EventManager.trigger("OpenPopUp", "NewTrainPopUp")
    
    def click_on_train(self, content) -> None:
        DataManager.current_train = content
        DataManager.current_exercice = 0
        EventManager.trigger("OpenScreen", "TrainInfoScreen")

    def on_pre_enter(self, *args):
        pass
    
    def on_leave(self, *args):
        pass
