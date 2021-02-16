from datetime import datetime as dt
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy import Integer, String, Float, Text, DateTime, Boolean, Date
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declared_attr, declarative_base


engine = create_engine('sqlite:///ulaanbataar.db')


class Base_:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=Base_)


class Series(Base):
    kind = Column(String)
    series = Column(Text)
    correlations = relationship("Correlation", backref="series")


class Correlation(Base):
    series_a = Column(Integer, ForeignKey(Series.id))
    series_b = Column(Integer, ForeignKey(Series.id))


def get_session():
    s = sessionmaker(bind=engine)
    return scoped_session(s)


Base.metadata.create_all(engine)
