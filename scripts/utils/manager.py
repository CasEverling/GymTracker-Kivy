from typing import Dict, List, Tuple
from collections import deque

from kivy.uix.screenmanager import Screen, ScreenManager

from screens.charts_screen.rought import RoughChartPopUp
from screens.new_exercice_screen.rought import RoughtNewExercicePopUp
from screens.new_train_screen.rought import RoughtNewTrainPopUp
from screens.train_info_screen.rougth import TrainInfoScreen
from screens.select_train_screen.rought import SelectTrainScreen
from screens.create_user_screen.rougth import RoughtNewUserPopUp
from screens.train_section_screen.rought import RoughtTrainSectionScreen

from scripts.utils.eventmanager import EventManager
from scripts.ui.popup import CEPopUp

class AppManager:

    current_screen: str = "ChartsScreen"
    current_user: int = 0

    screen_types: Dict[str,type] = {
        "TrainSelectionScreen": SelectTrainScreen,
        "TraiSectionScreen": RoughtTrainSectionScreen,
        "TrainInfoScreen": TrainInfoScreen,
    }

    popup_types: Dict[str,type] = {
        "ChartPopUp": RoughChartPopUp,
        "NewExercicePopUp": RoughtNewExercicePopUp,
        "NewTrainPopUp": RoughtNewTrainPopUp,
        "CreateUserPopUp": RoughtNewUserPopUp,
    }

    popups: Dict[str, CEPopUp] = {}
    screens: Dict[str, Screen] = {}
    screen_history: deque = deque()

    def __init__(self) -> None:
        EventManager.set_trigger("OpenPopUp", self.open_popup)
        EventManager.set_trigger("OpenScreen", self.access_screen)

    def access_screen(self, screen: str) -> None:
        print(screen)
        # checck whether the screen change is legal
        # move to screen
        try:
            EventManager.trigger("ChangeScreen", new_screen = self.screens[screen])
        except:
            self.screens[screen] = self.screen_types[screen]()
            EventManager.trigger("ChangeScreen", new_screen = self.screens[screen])
        # add screen to screen history
        
        pass

    def access_previous_screen(self) -> None:
        self.screen_history.pop()
        self.access_screen(self.screen_history.pop())
    
    def open_popup(self, popupName: str) -> None:
        try:
            EventManager.trigger("AddPopUp", popup = self.popups[popupName])
        except:
            self.popups[popupName] = self.popup_types[popupName]()
            EventManager.trigger("AddPopUp", popup = self.popups[popupName])



