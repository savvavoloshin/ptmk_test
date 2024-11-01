import argparse
import sqlite3
import datetime
import random
from datetime import datetime

from faker import Faker

def initialize_datatable(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS employees(name, birthdate, gender)")

class Employee:
    def __init__(self, name, birthdate, gender) -> None:
        self.name = name
        self.birthdate = birthdate
        self.gender = gender
    
    def compute_age(self):
        return datetime.date.today() - self.birthdate
    

    def store(self, connection):
        sql = ''' INSERT INTO employees(name, birthdate, gender)
              VALUES(?,?,?) '''
        cursor = connection.cursor()
        cursor.execute(sql, (self.name, self.birthdate, self.gender))
        connection.commit()
    
    @staticmethod
    def generate_a_million_objects():
        fake = Faker()
        employees = []
        for i in range(0, 1000000):
            name = "{} {} {}".format(fake.first_name(), fake.first_name(), fake.last_name())
            birthdate = fake.date_between()
            gender = random.choice(['Male','Female'])
            employee = Employee(name, birthdate, gender)
            employees.append(employee)
        print(len(employees))
        return employees
    
    @staticmethod
    def generate_a_hundred_objects():
        fake = Faker()
        employees = []
        for i in range(0, 100):
            name = "{} {} {}".format("F{}".format(fake.first_name().lower()), fake.first_name(), fake.last_name())
            birthdate = fake.date_between()
            gender = 'Male'
            employee = Employee(name, birthdate, gender)
            employees.append(employee)
        print(len(employees))
        return employees

    @staticmethod
    def store_objects(employees, connection):
        for employee in employees:
            sql = ''' INSERT INTO employees(name, birthdate, gender)
                VALUES(?,?,?) '''
            cursor = connection.cursor()
            cursor.execute(sql, (employee.name, employee.birthdate, employee.gender))
        connection.commit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("Test")
    parser.add_argument("choice", help="Choice must be an integer 1 to 5.", type=int)
    parser.add_argument("--name", help="Full name", type=str)
    parser.add_argument("--birthdate", help="Birth date: yyyy-mm-dd", type=str)
    parser.add_argument("--gender", help="Gender: Male/Female", type=str)
    args = parser.parse_args()

    connection = sqlite3.connect("example_31.db")
    
    # 1. Создание таблицы с полями справочника сотрудников, представляющими "Фамилию Имя Отчество", "дату рождения", "пол".
    if args.choice == 1:
        initialize_datatable(connection)

    # 2. Создание записи справочника сотрудников.
    # Для работы с данными создать класс и создавать объекты. При вводе создавать новый объект класса, с введенными пользователем данными.
    # При генерации строчек в базу создавать объект и его отправлять в базу/формировать строчку для отправки нескольких строк в БД.
    # У объекта должны быть методы, которые:
    # - отправляют объект в БД,
    # - рассчитывают возраст (полных лет).

    # Пример запуска во 2 режиме:
    # python employee.py 2 "Ivanov Petr Sergeevich" 2009-07-12 Male
    elif args.choice == 2:
        employee = Employee(args.name, args.birthdate, args.gender)
        employee.store(connection)

    # 3. Вывод всех строк справочника сотрудников, с уникальным значением ФИО+дата, отсортированным по ФИО. Вывести ФИО, Дату рождения, пол, кол-во полных лет.
    # Пример запуска приложения:
    # python employee.py 3
    elif args.choice == 3:
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT name, birthdate, gender FROM employees ORDER BY name")
        rows = cursor.fetchall()

        for row in rows:
            name = row[0]
            birthdate = row[1]
            gender = row[2]
            age = datetime.now() - datetime.strptime(birthdate, '%Y-%m-%d')
            print("{} {} {} {}".format(name, birthdate, gender, int(age.days/365)))
    
    # 4. Заполнение автоматически 1000000 строк справочника сотрудников. Распределение пола в них должно быть относительно равномерным, начальной буквы ФИО также. Добавить заполнение автоматически 100 строк в которых пол мужской и Фамилия начинается с "F".
    # У класса необходимо создать метод, который пакетно отправляет данные в БД, принимая массив объектов.
    # Пример запуска приложения:
    # python employee.py 4
    elif args.choice == 4:
        a_million = Employee.generate_a_million_objects()
        a_hundred = Employee.generate_a_hundred_objects()
        Employee.store_objects(a_million, connection)
        Employee.store_objects(a_hundred, connection)
    
    # 5. Результат выборки из таблицы по критерию: пол мужской, Фамилия начинается с "F". Сделать замер времени выполнения.
    # Пример запуска приложения:
    # python employee.py 5
    # Вывод приложения должен содержать время. Заполнить это время в отчете по выполнению тестового задания.
    elif args.choice == 5:
        t1 = datetime.now()
        
        cursor = connection.cursor()
        cursor.execute("SELECT name, birthdate, gender FROM employees WHERE gender == 'Male' AND name LIKE 'F%'")
        rows = cursor.fetchall()
        for row in rows:
            name = row[0]
            birthdate = row[1]
            gender = row[2]
            print("{} {} {}".format(name, birthdate, gender))
        
        t2 = datetime.now()
        print("Execution time: {}".format(t2-t1))
    else:
        print("wrong argument")
    
    connection.close()
        
