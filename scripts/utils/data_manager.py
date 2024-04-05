print('Hello World!')

from typing import List
from scripts.data_abstractions.user import User
from scripts.data_abstractions.train import Train
from scripts.data_abstractions.section import Section

class DataManager:
    current_users: List[User] = []
    current_user: int = 0
    current_train: Train = None
    current_exercice_index: int = 0
    current_section_ids: List[int] = []
    train_history: dict[int:float] = {}