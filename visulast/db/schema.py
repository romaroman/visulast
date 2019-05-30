from sqlalchemy import Column, ForeignKey, Integer, String, Date, Text, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('id', 'number')
    )

    id = Column(Integer, primary_key=True)
    lastfm_username = Column(String, nullable=False)
    telegram_id = Column(Integer, primary_key=True)
    start_timestamp = Column(Date, nullable=True)

    def __repr__(self):
        return "<User(last.fm username='%s', Telegram ID='%s', Dialog start time='%s')>" % (
            self.lastfm_username, self.telegram_id, self.start_timestamp)


class Result(Base):
    __tablename__ = 'results'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    request = Column(Text, nullable=True)
    obj_path = Column(Text, nullable=True)
    img_path = Column(Text, nullable=True)
    timestamp = Column(Date, nullable=True)

    user = relationship(User)


class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Date, nullable=True)
    level = Column(Integer, nullable=True)


class ArtistScrapped(Base):
    __tablename__ = 'artists_scrapped'

    id = Column(Integer, primary_key=True)
    mbid = Column(String, nullable=True)
    name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    info_source = Column(String, nullable=True)