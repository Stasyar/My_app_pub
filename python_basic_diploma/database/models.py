# -*- coding: utf-8 -*-
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, String, Column, DateTime, create_engine
from datetime import datetime

engine = create_engine(url="sqlite:///user_query.db", echo=True)

Base = declarative_base()


class UserQuery(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    query = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)


Session = sessionmaker(bind=engine)
session = Session()


def models_main():
    Base.metadata.create_all(engine)
