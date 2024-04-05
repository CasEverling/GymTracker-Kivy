print('Hello World!')
from typing import Generic, Dict, List
T = type[Generic]

class EventManager:
    __functions = {}

    @staticmethod
    def set_trigger(name: str, fun: T) -> None:
        try:
            EventManager.__functions[name].append(fun)
        except:
            EventManager.__functions[name] = [fun]
    
    @staticmethod
    def trigger(name:str, *args, **kwargs) -> T:
        try:
            for event in EventManager.__functions[name]:
                try:
                    event(*args, **kwargs)
                except Exception as e:
                    print(EventManager.__functions[name], *args)
                    print(e)
        except Exception as e:
            print(e)
        
