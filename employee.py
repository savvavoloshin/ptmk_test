import argparse
import sqlite3

def initialize_datatable(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS employees(name, birthdate, gender)")

class Employee:
    def __init__(self, name, birthdate, gender) -> None:
        self.name = name
        self.birthdate = birthdate
        self.gender = gender

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Test")
    parser.add_argument("choice", help="Choice must be an integer 1 to 3.", type=int)
    args = parser.parse_args()

    connection = sqlite3.connect("example_31.db")
    cursor = connection.cursor()
    
    if args.choice == 1:
        initialize_datatable(cursor)
    elif args.choice == 2:
        print(args.choice)
    elif args.choice == 3:
        print(args.choice)
    else:
        print("wrong argument")
        
