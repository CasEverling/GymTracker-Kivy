print("Hello World!")

from dataclasses import dataclass
from typing import List
from scripts.data_abstractions.train import Train


@dataclass
class Section:
    section_id: int
    user_id: int
    train: Train
    metrics: List[float]