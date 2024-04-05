def show_exercice_history():
    pass

def show_compared_trains():
    pass

def show_predicted_waight():
    pass

def create_barplot():
    pass

from typing import Dict, Tuple
import seaborn
import matplotlib.pyplot as plt

def draw_exercice_history_plot(exercice_id: int, user_id: int):
    pass

def build_bar_chart(data: Dict[str,int], title: str, x_label: str, y_label: str, size: Tuple[float, float]):
    print('creating_figure')
    plt.figure(figsize=(size))
    print('setting_colors')
    seaborn.set_palette(["black"])
    print('Adding_data')
    plt.bar(data.keys(), data.values())
    print('\n\n\n\n\n\n\n\n\n\n')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    print('exporting')
    plt.savefig('imaadsage.png')
    plt.close()
    print('exported')


if __name__ == '__main__':
    print('Hello World!')
    build_bar_chart(
        {'a':1,'b':2, 'c':10,'dasd':1,"de":90,'a1':1,'b2':2, 'c3':10,'dasd1':1,"de1":90,'a2':1,'b1':2, 'c2':10,'dasd':1,"de":90,'a':1,'b':2, 'c':10,'dasd':1,"de":90}, 
        "peso por dias", "dias", "peso", (10,5))


