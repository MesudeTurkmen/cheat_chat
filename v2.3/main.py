import os
import sqlalchemy
from sqlalchemy import create_engine, event, Engine
from sqlalchemy.orm import scoped_session, sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

engine = create_engine(f'sqlite:///{BASE_DIR}/db', echo=True)

session = scoped_session(
    sessionmaker(
        autoflash=False,
        autocommint=False,
        bind=engine
    )
)


@event.listens_for(Engine, 'connect')
def set_sqlite_prgame(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA  foreing_keys=ON')
    cursor.close()

