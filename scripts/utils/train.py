print("Hello World!")
import sqlite3
import os
from typing import List, Tuple, Dict
from collections import defaultdict
# Wrappers

from scripts.data_abstractions.user import User
from scripts.data_abstractions.train import Train
from scripts.data_abstractions.exercice import Exercice
from scripts.data_abstractions.section import Section

def change_database(fun):
    def updated_function(*args, **kwargs):
        if "cursor" in kwargs:
            return fun(*args, **kwargs)
        db = sqlite3.connect("trains.db")
        cursor = db.cursor()
        return_value = fun(*args, **kwargs, cursor = cursor)
        db.commit()        
        db.close()
        return return_value
    return updated_function

def read_database(fun):
    def updated_function(*args, **kwargs):
        if "cursor" in kwargs:
            return fun(*args, **kwargs)
        db = sqlite3.connect("trains.db")
        cursor = db.cursor()
        return_value =  fun(*args, **kwargs, cursor = cursor)
        db.close()
        return return_value
    return updated_function

# Functions that create the tables

@change_database
def create_all_tables(cursor: sqlite3.Cursor = None):
    create_users_table(cursor = cursor)
    create_trains_table(cursor = cursor)
    create_exercices_table(cursor = cursor)
    create_train_exercices_table(cursor = cursor)
    create_train_assignment_table(cursor = cursor)
    create_sections_table(cursor = cursor)
    create_section_info_table(cursor = cursor)

@change_database
def create_users_table(cursor: sqlite3.Cursor = None):
   cursor.execute("CREATE TABLE IF NOT EXISTS Users (user_id int, name str)") 

@change_database
def create_trains_table(cursor: sqlite3.Cursor = None):
    cursor.execute("CREATE TABLE IF NOT EXISTS Trains (train_id int, title str, description str)") 

@change_database
def create_exercices_table(cursor: sqlite3.Cursor = None):
    cursor.execute("CREATE TABLE IF NOT EXISTS Exercices (exercice_id int, name str, description str, metric str)") 

@change_database
def create_train_exercices_table(cursor: sqlite3.Cursor = None):
    cursor.execute("CREATE TABLE IF NOT EXISTS TrainExercices (train_id int, exercice_id int)") 

@change_database
def create_train_assignment_table(cursor: sqlite3.Cursor = None):
    cursor.execute("CREATE TABLE IF NOT EXISTS TrainAssignments (train_id int, user_id int)") 

@change_database
def create_section_info_table(cursor: sqlite3.Cursor = None):
    cursor.execute("CREATE TABLE IF NOT EXISTS SectionInfo (section_id int, exercice_id int, metric float)")

@change_database
def create_sections_table(cursor: sqlite3.Cursor = None):
    cursor.execute("CREATE TABLE IF NOT EXISTS TrainSections (section_id int, user_id int, train_id int)") 



# Functions that change the database
@change_database
def add_user(name: str,  cursor: sqlite3.Cursor = None) -> int:
    user_id: int = None

    # Get the id of the new train
    cursor.execute("SELECT MAX(user_id) FROM Users")
    user_id = (previous + 1)  if (previous := cursor.fetchone()[0]) != None else 0

    cursor.execute("INSERT INTO Users (user_id, name) VALUES (?, ?)",(user_id, name))

    return user_id

@change_database
def create_train(title: str, description: str, exercice_ids: List[int] = [], cursor: sqlite3.Cursor = None) -> int:
    train_id: int = None

    # Get the id of the new train
    cursor.execute("SELECT MAX(train_id) FROM Trains")
    train_id = (previous + 1)  if (previous := cursor.fetchone()[0]) != None else 0

    # Creates New Train Id - Table Trains
    cursor.execute("INSERT INTO Trains (train_id, title, description) VALUES (?, ?, ?)",(train_id, title, description))

    # Adds Exercices For This train Id - Table TrainExercices
    add_exercices_to_train(train_id, exercice_ids, cursor=cursor)
    return train_id

@change_database
def add_exercice(name: str, description: str, metric: str, cursor: sqlite3.Cursor = None) -> int:
    exercice_id: int = None

    # Get the id of the new exercice
    cursor.execute("SELECT MAX(exercice_id) FROM Exercices")
    exercice_id = (previous + 1)  if (previous := cursor.fetchone()[0]) != None else 0

    # Adds Exercices For an exercice list - Table Exercices
    cursor.execute("INSERT INTO Exercices (exercice_id, name, description, metric) VALUES (?, ?, ?, ?)", (exercice_id, name, description, metric))
    
    return exercice_id

@change_database
def add_exercices_to_train(train_id: int, exercice_ids: List[int], cursor: sqlite3.Cursor = None) -> None:
    # Adds Exercices For This train Id - Table TrainExercices
    for exercice_id in exercice_ids:
        cursor.execute("INSERT INTO TrainExercices (train_id, exercice_id) VALUES (?, ?)", (train_id, exercice_id))

@change_database
def remove_exercice_from_train(train_id: int, exercice_id: int, cursor: sqlite3.Cursor = None) -> None:
    # Removes Exercices For This train Id - Table Exercices
    pass

@change_database
def assing_train(train_id: int, user_id: int, cursor: sqlite3.Cursor = None) -> None:
    cursor.execute("INSERT INTO TrainAssignments (train_id, user_id) VALUES (?, ?)", (train_id, user_id))

@change_database
def create_section(user_id: int, train_id: int, cursor: sqlite3.Cursor = None) -> int:
    # Creates a train section - Table TrainSections
    section_id: int = None
    cursor.execute("SELECT MAX(section_id) FROM TrainSections")
    section_id = (previous + 1)  if (previous := cursor.fetchone()[0]) != None else 0
    cursor.execute("INSERT INTO TrainSections (section_id, user_id, train_id) VALUES (?,?,?)", (section_id, user_id, train_id))

    # Sets the metrics of all exercices to 0  - Table SectionsInfo
    for exercice in get_train(train_id, cursor = cursor).exercices:
        add_section_info(section_id, exercice, cursor = cursor)
    
    return section_id

@change_database
def add_section_info(section_id: int, exercice_id: int, cursor: sqlite3.Cursor = None) -> None:
    # Add Exercice Info - Table SectionsInfo
    cursor.execute(
        "INSERT INTO SectionInfo (section_id, exercice_id, metric) VALUES (?,?,?)", 
        (section_id, exercice_id, 0)
        )

@change_database
def edit_section_info(section_id: int, exercice_id: int, metric: float, cursor: sqlite3.Cursor = None) -> None:
    cursor.execute(
        "UPDATE SectionInfo SET metric = ?  WHERE section_id = ? AND exercice_id = ?", 
        (metric, section_id, exercice_id)
        )


# Functions that read the database

@read_database
def get_trains(user_ids: List[int], cursor: sqlite3.Cursor = None) -> List[Train]:
    #get the train ids from each user
    train_ids_count: Dict[str,int] = {}
    common_train_ids: List[int] = []
    common_trians: List[Train] = []

    # Get common train ids
    for user_id in user_ids:
        cursor.execute("SELECT * FROM TrainAssignments WHERE user_id = ?", (user_id,))
        for train_id, _ in cursor.fetchall():
            print(train_id)
            try:
                train_ids_count[train_id] += 1
            except:
                train_ids_count[train_id] = 1
            if train_ids_count[train_id] == len(user_ids):
                common_train_ids.append(train_id)
    
    print(train_ids_count)
    # Get common trains info
    for train_id in common_train_ids:
        if train_id == None:
            continue
        common_trians.append(get_train(train_id, cursor=cursor))
    
    return common_trians

@read_database
def get_train(train_id: int, cursor: sqlite3.Cursor = None) -> Train:
    cursor.execute("SELECT title, description FROM Trains WHERE train_id = ?", (train_id,))
    title, desctiption = cursor.fetchone()
    cursor.execute("SELECT exercice_id FROM TrainExercices WHERE train_id = ?", (train_id,))
    exercices =  cursor.fetchall()
    return Train(
        train_id,
        title,
        desctiption,
        [exercice[0] for exercice in exercices]
    )

@read_database
def get_section(section_id: int, cursor: sqlite3.Cursor = None) -> Section:
    cursor.execute("SELECT (user_id, train_id) FROM TrainSections WHERE section_id = ?", (section_id,))
    user_id, train_id = cursor.fetchone()

    cursor.execute("SELECT (metric) FROM SectionInfo WHERE section_id = ?", (section_id,))
    metrics = cursor.fetchall()

    return Section(
        section_id,
        user_id,
        get_train(train_id),
        [metric[0] for metric in metrics],
    )

@read_database
def get_exercice(exercice_id: int, cursor: sqlite3.Cursor = None) -> Exercice:
    cursor.execute("SELECT * FROM Exercices WHERE exercice_id = ?", (exercice_id,))
    return Exercice(*cursor.fetchone())

@read_database
def get_all_users(cursor: sqlite3.Cursor = None) -> List[User]:
    cursor.execute("SELECT * FROM Users")
    return [
        User(user_id = user_info[0], name = user_info[1]) for user_info in cursor.fetchall()
    ]

@read_database
def get_exercice_history(user_id: int, exercice_id: int, cursor: sqlite3.Cursor = None) -> List[float]:
    cursor.execute("SELECT metric FROM SectionInfo WHERE exercice_id = ? AND section_id IN (SELECT section_id FROM TrainSections WHERE user_id = ?)", (exercice_id, user_id))
    return [info[0] for info in cursor.fetchall()]

if __name__ == '__main__':
    pass