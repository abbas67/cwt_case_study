"""
Basic module to load data from csv files and dump into sql database.
"""

import pandas as pd
from sqlalchemy import MetaData, Table, Column, Integer, String

from cwt_case_study.db_utils import new_engine, DATABASE_FILE

engine = new_engine()


def create_tables():
    """
    Creates tables using sqlalchemy MetaData class.
    :return: N/A
    """

    meta = MetaData()
    Table(
        'reviews', meta,
        Column('ClothingID', Integer),
        Column('Age', Integer),
        Column('Title', String),
        Column('ReviewText', String),
        Column('Rating', Integer),
        Column('RecommendedIND', Integer),
        Column('PositiveFeedbackCount', Integer),
        Column('DivisionName', String),
        Column('DepartmentName', String),
        Column('ClassName', String)
    )

    meta.create_all(engine)


def insert_into_table():
    """
    Inserting data into tables using pandas.
    :return: N/A
    """

    df = pd.read_csv(DATABASE_FILE).iloc[:, 1:]
    df.to_sql("reviews", engine, if_exists='replace')


if __name__ == '__main__':
    create_tables()
    insert_into_table()
