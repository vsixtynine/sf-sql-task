# Imports
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import users
from datetime import datetime

"""
Модуль для поиска атлетов по парамтрам пользователя
"""
# Variables
Base = declarative_base()

# Class definitions


class Athlette(Base):
    __tablename__ = "Athelete"
    id = sa.Column(sa.INTEGER, primary_key=True)
    age = sa.Column(sa.INTEGER)
    birthdate = sa.Column(sa.TEXT)
    gender = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)
    name = sa.Column(sa.TEXT)
    weight = sa.Column(sa.INTEGER)
    gold_medals = sa.Column(sa.INTEGER)
    silver_medals = sa.Column(sa.INTEGER)
    bronze_medals = sa.Column(sa.INTEGER)
    total_medals = sa.Column(sa.INTEGER)
    sport = sa.Column(sa.TEXT)
    country = sa.Column(sa.TEXT)


# Function definitions
def search_id(id, session):
    query_str = session.query(Athlette).filter(Athlette.id == id).first()
    usr = f"{query_str}"
    return usr


def height_compare(id, session, bcolors):
    """
    Сравнение роста атлетов с пользовательским
    """
    # берем из базы рост пользователя
    usr_query = session.query(users.User).filter(users.User.id == id).first()
    usr_height = usr_query.height

    # ищем атлетов по росту пользователя
    ath_query = session.query(Athlette).filter(
        Athlette.height == usr_height)

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
              f"\nERROR: Атлет с ростом {usr_height}m не найден" + bcolors.ENDC)

    return res


def bday_compare(id, session):
    """
    Ищем атлета, наиболее близкого по дате рождения к пользователю
    """
    dt_format = '%Y-%m-%d'
    usr_query = session.query(users.User).filter(users.User.id == id).first()
    user_bday_str = usr_query.birthdate
    user_bday_dt_obj = datetime.strptime(user_bday_str, dt_format)

    ath_query_all_obj = session.query(Athlette).all()

    ath_bday_all_dt_list = list()
    for ath in ath_query_all_obj:
        ath_bday_all_dt_list.append(
            datetime.strptime(ath.birthdate, dt_format))

    closest_bday_dt_obj = ath_bday_all_dt_list[min(range(len(ath_bday_all_dt_list)),
                                                   key=lambda i: abs(ath_bday_all_dt_list[i]-user_bday_dt_obj))]

    # выбираем всех атлетов по самой ближней дате рождения
    closest_bday_str = closest_bday_dt_obj.strftime(dt_format)
    ath_query_bday_query = session.query(Athlette).filter(
        Athlette.birthdate == closest_bday_str)

    # берем из базы данные и считаем
    ath_bday_obj = ath_query_bday_query.all()
    ath_bday_count = ath_query_bday_query.count()

    # формируем возврат
    res = ""
    for ath in ath_bday_obj:
        res = f"{res}\n  {ath.name}, д.р.: {ath.birthdate}, {ath.sport}"

    return res


if __name__ == "__main__":
    print("ERROR: Запуск скрипта через выполнение модуля start.py \n")


# DEBUG
# print('Info: Module find_athlete.py - imported')
