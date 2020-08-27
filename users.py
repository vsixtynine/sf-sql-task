# Базовый класс моделей таблиц
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa

Base = declarative_base()

# Variables


# Class definitions
class User(Base):
    __tablename__ = "user"
    id = sa.Column(sa.INTEGER, primary_key=True)
    first_name = sa.Column(sa.TEXT)
    last_name = sa.Column(sa.TEXT)
    email = sa.Column(sa.TEXT)
    birthdate = sa.Column(sa.TEXT)
    height = sa.Column(sa.REAL)


# Function definitions
def add(session, bcolors):

    print(bcolors.OKGREEN +
          "\n  Добавяем пользователя в БД:\n" + bcolors.ENDC)

    first_name = str(input("Имя: ")).capitalize()
    last_name = str(input("Фамилия: ")).capitalize()
    email = str(input("Email: ")).lower()
    birthdate = str(input("Дата рожения (YYYY-MM-DD): "))  # YYYY-MM-DD
    height = str(input("Рост (м): ")).replace(",", ".")

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        birthdate=birthdate,
        height=height
    )

    session.add(user)
    session.commit()

    # проверяем по фамилии успешное добавление и выводим сообщение с ID
    usr = find_name(last_name, session)
    if usr:
        print(bcolors.OKGREEN +
              f"\n  Пользователь {usr} - успешно добавлен" + bcolors.ENDC)
    else:
        print(bcolors.FAIL +
              f"\nERROR: Не удалось внести пользователя в БД" + bcolors.ENDC)


def find_id(id, session):
    query_str = session.query(User).filter(User.id == id).first()
    if query_str:
        result = f"{query_str.first_name} {query_str.last_name} \
             \n                 Рост: {query_str.height} \
             \n        Дата рождения: {query_str.birthdate}"
    else:
        result = None
    return result


def find_name(name, session):
    query_str = session.query(User).filter(User.last_name == name).first()

    result = f"{query_str.first_name} {query_str.last_name} [ID: {query_str.id}]"
    return result


if __name__ == "__main__":
    print("ERROR: Запуск скрипта через выполнение модуля start.py \n")


# DEBUG
# print('Info: Module users.py - imported')
