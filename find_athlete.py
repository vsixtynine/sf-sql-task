# Imports
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

"""
Module for finding a closest athlete.
"""
# Variables
Base = declarative_base()

# Class definitions

"""
athelete(
    "id" integer primary key autoincrement,
    "age" integer,
    "birthdate" text,
    "gender" text,
    "height" real,
    "name" text,
    "weight" integer,
    "gold_medals" integer,
    "silver_medals" integer,
    "bronze_medals" integer,
    "total_medals" integer,
    "sport" text,
    "country" text);
"""


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
    query = session.query(Athlette).filter(Athlette.id == id).first()
    usr = f"{query}"
    return usr


if __name__ == "__main__":
    print("\ERROR: Запуск скрипта через выполнение модуля start.py \n")


# DEBUG

print('Info: Module find_athlete.py - imported')
