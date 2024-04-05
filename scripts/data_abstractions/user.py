from dataclasses import dataclass

@dataclass
class User:
    name: str
    user_id: int

    def __str__(self):
        return self.name

