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
    kind = Column(String)       # this will have to be a type system we create
    series = Column(Text)       # a json object of timeseries data
    first = Column(Date)        # the first date in the series
    last = Column(Date)         # the last date in the series

    @property
    def correlations(self):
        return self.corr_a + self.corr_b

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<Series {self.kind} {self.first} {self.last}>"

class Correlation(Base):
    series_a = Column(Integer, ForeignKey(Series.id))
    series_b = Column(Integer, ForeignKey(Series.id))
    score = Column(Float)       # pearson * lag
    pearson = Column(Float)
    lag = Column(Integer)       # positive a leads, negative b leads

    a = relationship("Series", backref="corr_a", foreign_keys=[series_a])
    b = relationship("Series", backref="corr_b", foreign_keys=[series_b])

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"<Correlation {self.a.kind} {self.b.kind} {self.score}>"


def get_session():
    s = sessionmaker(bind=engine)
    return scoped_session(s)


Base.metadata.create_all(engine)
