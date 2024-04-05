from dataclasses import dataclass
from typing import List

@dataclass
class Train:
    train_id: int
    title: str
    description: str
    exercices: List[int]

    def __str__(self):
        return self.title