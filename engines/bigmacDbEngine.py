from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from datetime import datetime

from helpers.dateConverter import dateToStringFormat


class BigmacDatabaseEngine():
    def __init__(self, url:str, prompt=False):
        self.url = url
        self.prompt = prompt

        self.engine = None
        self.metadata = MetaData()
        self.connection = None

        self.table = None
        self.__connect()

    def store(self, country:str, from_date:datetime, to_date:datetime, records:list):
        from_date = dateToStringFormat(from_date)
        to_date = dateToStringFormat(to_date)
        records = ', '.join(str(i) for i in records)

        query = self.table.insert().values(
            country = country,
            from_date = from_date,
            to_date = to_date,
            records = records
        )
        self.connection.execute(query)

        return True

    def isRecordExist(self, country):
        query = self.table.select().where(self.table.c.country==country)
        return bool(self.connection.execute(query).fetchone())

    def queryAll(self):
        query = self.table.select()
        return self.connection.execute(query).fetchall()

    def close(self):
        self.engine.dispose()

    def __connect(self):
        self.engine = create_engine(self.url, echo=self.prompt)

        self.table = Table(
            'bigmac', self.metadata,
            Column('id', Integer, primary_key=True),
            Column('country', String),
            Column('from_date', String),
            Column('to_date', String),
            Column('records', String)
        )

        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()

