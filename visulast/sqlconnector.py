import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from config import Configuration

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    lastfm_username = Column(String(250), nullable=False)
    # telegram_id = Column(Integer, primary_key=True)


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    update_date = Column(Date, nullable=False)
    limit = Column(Integer, nullable=False)
    library = Column(LargeBinary, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User)


if __name__ == "__main__":
    engine = create_engine(
        Configuration('postgresql').get_sql_url())
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)
