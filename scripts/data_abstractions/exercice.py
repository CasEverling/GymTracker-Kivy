from dataclasses import dataclass

@dataclass
class Exercice:
    exercice_id: int
    name: str
    description: str
    metric: str
    
    def __str__(self):
        return self.name