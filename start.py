
# Imports
import users
import find_athlete
import sys
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import uuid
import datetime

# Global variables
task = """    Задание №1:

 Напишите модуль users.py, который регистрирует новых пользователей. Скрипт должен запрашивать следующие данные:

    * имя
    * фамилию
    * пол
    * адрес электронной почты
    * дату рождения
    * рост

------------------
    Задание 2

Напишите модуль find_athlete.py поиска ближайшего к пользователю атлета. Логика работы модуля такова:

    * запросить идентификатор пользователя;
    * если пользователь с таким идентификатором существует в таблице user,
      то вывести на экран двух атлетов: ближайшего по дате рождения к данному пользователю
      и ближайшего по росту к данному пользователю;
    * если пользователя с таким идентификатором нет, вывести соответствующее сообщение.
"""


DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()


# Class definitions
class bcolors:
    HEADER = '\033[96m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Function definitions
def connect_db():
    # create connection
    engine = sa.create_engine(DB_PATH)

    # create tables
    Base.metadata.create_all(engine)

    # create session fabric
    session = sessionmaker(engine)

    # Return session
    return session()


def choose_mode():
    print(bcolors.HEADER + "\n---------------------------------------------")
    print("   Модуль B4, домашнее задание: \n")
    print(bcolors.BOLD + " [1] Добавить пользователя в базу /задание №1/")
    print(bcolors.BOLD +
          " [2] Похожие на пользователя атлеты /задание №2/\n   " + bcolors.ENDC)
    print(bcolors.HEADER + " [3] Найти пользователя по ID")
    print(" [4] Найти атлета похожего по возрасту на пользователя")
    print(" [5] Найти атлета похожего по росту на пользователя\n   ")
    print(" [6] Вывести условия задачи\n   ")
    print(" [7] Выход\n")
    print("---------------------------------------------" + bcolors.ENDC)

    while True:
        mode = input("\nВыберите, пожалуйста, пункт меню: ")
        try:
            mode = int(mode)
        except ValueError:
            print(bcolors.FAIL + "ERROR: Необходимо ввести номер пункта" + bcolors.ENDC)
            continue
        if 1 <= mode <= 7:
            break
        else:
            print(bcolors.FAIL + "ERROR: Такого пункта не существует" + bcolors.ENDC)

    return mode


def input_request(mode):
    """"
    Запрашивает и результирует данные
    """
    session = connect_db()

    if mode == 1:
        """
        Пункт меню: добавление пользователя в базу
        """
        # DONE

        users.add(session, bcolors())

    if mode == 2:
        """
        Вывод по заданию
        """
        print(bcolors.OKGREEN +
              "\n  Ищем атлетов - ближайших ровесников пользователя," +
              "\n  а также атлетов одинакового с пользователем роста.\n" + bcolors.ENDC)

        id = id_ask()
        res = users.find_id(id, session)
        if res:
            print(bcolors.OKGREEN +
                  f"\n  Найден пользователь: {res}" + bcolors.ENDC)

            # Ищем ближайших ровесников
            ath_str = find_athlete.bday_compare(id, session)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
            print(bcolors.OKGREEN +
                  f"\n  Самые близкие ровесники - атлеты: \n{ath_str}" + bcolors.ENDC)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

            ath_str = find_athlete.height_compare(id, session, bcolors())
            if ath_str != "":
                print(bcolors.OKGREEN +
                      f"  Атлеты с одинаковым ростом:\n" + bcolors.ENDC)
                # input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
                print(bcolors.OKGREEN + f"{ath_str}" + bcolors.ENDC)
                input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
            else:
                input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

        else:
            print(bcolors.FAIL +
                  f"ERROR: Пользователь с ID:{id} не найден" + bcolors.ENDC)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

    if mode == 3:
        """
        Пункт меню: поиск пользователя по ID
        """
        # DONE

        print(bcolors.OKGREEN + "\n  Ищем пользователя по ID:\n" + bcolors.ENDC)

        id = id_ask()

        res = users.find_id(id, session)
        if res:
            print(bcolors.OKGREEN +
                  f"\n  Найден пользователь: {res}" + bcolors.ENDC)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

        else:
            print(bcolors.FAIL +
                  f"\nERROR: Пользователь с ID:{id} не найден" + bcolors.ENDC)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

    if mode == 4:
        """
        Поиск атлета по параметрам даты рождения пользователя
        """

        print(bcolors.OKGREEN +
              "\n  Ищем атлета по параметрам даты рождения пользователя:\n" + bcolors.ENDC)

        id = id_ask()

        res = users.find_id(id, session)
        if res:
            print(bcolors.OKGREEN +
                  f"\n  Найден пользователь: {res}" + bcolors.ENDC)

            # Ищем подходящих атлетов:
            ath = find_athlete.bday_compare(id, session)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
            print(bcolors.OKGREEN +
                  f"\n  Самые близкие ровесники: \n{ath}" + bcolors.ENDC)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
        else:
            print(bcolors.FAIL +
                  f"\nERROR: Пользователь с ID:{id} не найден" + bcolors.ENDC)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

    if mode == 5:
        """
        Поиск атлета по параметрам роста пользователя
        """

        print(bcolors.OKGREEN +
              "\n  Ищем атлета по параметрам пользователя:\n" + bcolors.ENDC)

        id = id_ask()

        res = users.find_id(id, session)
        if res:
            print(bcolors.OKGREEN +
                  f"\n  Найден пользователь: {res}" + bcolors.ENDC)

            # Ищем подходящего атлета:
            ath = find_athlete.height_compare(id, session, bcolors())
            if ath != "":
                input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
                print(bcolors.OKGREEN + f"{ath}" + bcolors.ENDC)
                input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
            else:
                input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

        else:
            print(bcolors.FAIL +
                  f"\nERROR: Пользователь с ID:{id} не найден" + bcolors.ENDC)

            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

    if mode == 6:
        print(bcolors.OKBLUE + "\n" + task + bcolors.ENDC)
        input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

    if mode == 7:
        print(bcolors.WARNING + bcolors.BOLD +
              "\nХорошего дня!\n" + bcolors.ENDC)
        sys.exit(0)

    return 0


def id_ask():
    while True:
        id_raw = input("Введите ID пользователя: ")
        try:
            answer = int(id_raw)
        except ValueError:
            print(bcolors.FAIL + "ERROR: Необходимо ввести номер ID\n" + bcolors.ENDC)
            continue
        if answer > 0:
            break
        else:
            print(bcolors.FAIL + "ERROR: Такого ID не существует\n" + bcolors.ENDC)

    return answer


def main():
    """
    Launcher.
    """
    while True:
        input_request(choose_mode())


if __name__ == "__main__":
    main()


# DEBUG
