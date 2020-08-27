# Базовый класс моделей таблиц
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa

Base = declarative_base()


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


def input_data():
    pass


def add():
    pass


def find_id(id, session):
    query = session.query(User).filter(User.id == id).first()
    if query:
        result = f"{query.first_name} {query.last_name}"
    else:
        result = None
    return result


def find_name(name, session):
    query = session.query(User).filter(User.last_name == name).first()

    result = f"{query.first_name} {query.last_name} [ID: {query.id}]"
    return result


# def list():
#     pass


def remove():
    pass


if __name__ == "__main__":
    print("\ERROR: Запуск скрипта через выполнение модуля start.py \n")


# DEBUG
print('Info: Module users.py - imported')
