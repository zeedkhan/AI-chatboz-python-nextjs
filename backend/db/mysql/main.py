from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session as BaseSession
from backend.schemas.user import Base as UserBase

DATABASE_URL = "mysql://username:password@db_mysql:3306/main"


def create_database_session() -> BaseSession:
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def create_tables():
    engine = create_engine(DATABASE_URL)
    UserBase.metadata.create_all(bind=engine)


create_tables()