from typing import Dict, Tuple
import seaborn
import matplotlib.pyplot as plt

def draw_exercice_history_plot(exercice_id: int, user_id: int):
    pass

def build_bar_chart(data: Dict[str,int], title: str, x_label: str, y_label: str, size: Tuple[float, float]):
    plt.figure(figsize=(size))
    seaborn.set_palette(["black"])
    plt.bar(data.keys(), data.values())
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.savefig('image.png')


if __name__ == '__main__':
    print('Hello World!')
    build_bar_chart(
        {'a':1,'b':2, 'c':10,'dasd':1,"de":90,'a1':1,'b2':2, 'c3':10,'dasd1':1,"de1":90,'a2':1,'b1':2, 'c2':10,'dasd':1,"de":90,'a':1,'b':2, 'c':10,'dasd':1,"de":90}, 
        "peso por dias", "dias", "peso", (10,5))