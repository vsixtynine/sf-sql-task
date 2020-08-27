"""
    Задание №1:
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
    print(" Меню: \n")
    print(" 1 - Добавить пользователя в базу")
    print(" 2 - Найти пользователя по ID")
    print(" 3 - Найти атлета похожего по росту на пользователя базы")
    print(" 4 - [x] Найти атлета похожего по возрасту на пользователя базы")
    print(bcolors.BOLD + "\n 5 - Выход\n")
    print("---------------------------------------------" + bcolors.ENDC)

    while True:
        mode = input("\nВыберите, пожалуйста, пункт меню: ")
        try:
            mode = int(mode)
        except ValueError:
            print(bcolors.FAIL + "ERROR: Необходимо ввести номер пункта" + bcolors.ENDC)
            continue
        if 1 <= mode <= 5:
            break
        else:
            print(bcolors.FAIL + "ERROR: Такого пункта не существует" + bcolors.ENDC)

    return mode


def input_request(mode):
    """"
    Запрашивает и результирует данные
    """
    if mode == 1:
        """
        Пункт меню: добавление пользователя в базу
        """
        session = connect_db()

        print(bcolors.OKGREEN + "\n  Добавяем пользователя в БД:\n" + bcolors.ENDC)

        first_name = str(input("Имя: ")).capitalize()
        last_name = str(input("Фамилия: ")).capitalize()
        email = str(input("Email: ")).lower()
        birthdate = str(input("Дата рожения (YYYY-MM-DD): "))  # YYYY-MM-DD
        height = str(input("Рост (м): ")).replace(",", ".")

        user = users.User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            birthdate=birthdate,
            height=height
        )

        session.add(user)
        session.commit()

        # проверяем по фамилии успешное добавление и выводим сообщение с ID
        usr = users.find_name(last_name, session)
        if usr:
            print(bcolors.OKGREEN +
                  f"\n  Пользователь {usr} - успешно добавлен" + bcolors.ENDC)
        else:
            print(bcolors.FAIL +
                  f"\nERROR: Не удалось внести пользователя в БД" + bcolors.ENDC)

    if mode == 2:
        """
        Пункт меню: поиск пользователя по ID
        """
        session = connect_db()

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

    if mode == 3:
        """
        Поиск атлета по параметрам роста пользователя
        """
        session = connect_db()

        print(bcolors.OKGREEN +
              "\n  Ищем атлета по параметрам пользователя:\n" + bcolors.ENDC)

        id = id_ask()

        res = users.find_id(id, session)
        if res:
            print(bcolors.OKGREEN +
                  f"\n  Найден пользователь: {res}" + bcolors.ENDC)
            # Ищем подходящего атлета:
            ath = user_compare(id, session)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
            print(bcolors.OKGREEN + f"{ath}" + bcolors.ENDC)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
        else:
            print(bcolors.FAIL +
                  f"\nERROR: Пользователь с ID:{id} не найден" + bcolors.ENDC)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

    if mode == 4:
        """
        Поиск атлета по параметрам даты рождения пользователя
        """
        session = connect_db()

        print(bcolors.OKGREEN +
              "\n  Ищем атлета по параметрам даты рождения пользователя:\n" + bcolors.ENDC)

        id = id_ask()

        res = users.find_id(id, session)
        if res:
            print(bcolors.OKGREEN +
                  f"\n  Найден пользователь: {res}" + bcolors.ENDC)

            # Ищем подходящих атлетов:
            ath = bday_compare(id, session)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
            print(bcolors.OKGREEN +
                  f"\n  Самые близкие ровесники: \n{ath}" + bcolors.ENDC)
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)
        else:
            print(f"\nERROR: Пользователь с ID:{id} не найден")
            input(bcolors.WARNING + "\n  [Enter]\n" + bcolors.ENDC)

    if mode == 5:
        print(bcolors.WARNING + bcolors.BOLD +
              "\nХорошего дня!\n" + bcolors.ENDC)
        sys.exit(0)

    return 0


def user_compare(id, session):

    # берем из базы рост пользователя
    usr_query = session.query(users.User).filter(users.User.id == id).first()
    usr_height = usr_query.height

    print(bcolors.OKGREEN +
          f"                 Рост: {usr_height}m" + bcolors.ENDC)

    # ищем атлетов по росту пользователя
    ath_query = session.query(find_athlete.Athlette).filter(
        find_athlete.Athlette.height == usr_height)

    ath_count = ath_query.count()
    ath_found = ath_query.all()

    # выводим содержимое объектов Athlete, если найдены
    res = ""
    if ath_found:
        for ath in ath_found:
            res += f"  {ath.name}, {ath.sport} \n"
        res = f"{res}\n  Всего атлетов с ростом {ath.height} метра: {ath_count}"
    else:
        print(bcolors.FAIL +
              "ERROR: Атлет с ростом {usr_height} не найден" + bcolors.ENDC)

    return res


def bday_compare(id, session):
    """
    Ищем атлета, наиболее близкого по дате рождения к пользователю
    """
    dt_format = '%Y-%m-%d'
    usr_query = session.query(users.User).filter(users.User.id == id).first()
    user_bday_str = usr_query.birthdate
    user_bday_dt_obj = datetime.datetime.strptime(user_bday_str, dt_format)
    print(bcolors.OKGREEN +
          f"        Дата рождения: {user_bday_str}\n" + bcolors.ENDC)

    ath_query_all_obj = session.query(find_athlete.Athlette).all()

    ath_bday_all_dt_list = list()
    for ath in ath_query_all_obj:
        ath_bday_all_dt_list.append(
            datetime.datetime.strptime(ath.birthdate, dt_format))

        # print('INFO:', ath_bday_all_dt_list)
    closest_bday_dt_obj = ath_bday_all_dt_list[min(range(len(ath_bday_all_dt_list)),
                                                   key=lambda i: abs(ath_bday_all_dt_list[i]-user_bday_dt_obj))]
    #print('closest_bday_list', type(closest_bday_dt_obj))

    # выбираем всех атлетов по самой ближней дате рождения
    closest_bday_str = closest_bday_dt_obj.strftime(dt_format)
    ath_query_bday_query = session.query(
        find_athlete.Athlette).filter(find_athlete.Athlette.birthdate == closest_bday_str)

    ath_bday_obj = ath_query_bday_query.all()
    ath_bday_count = ath_query_bday_query.count()

    res = ""
    for ath in ath_bday_obj:
        res = f"{res}\n  {ath.name}, д.р.: {ath.birthdate}"
    res = f"{res}\n\n  Всего найдено: {ath_bday_count}"

    return res


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
