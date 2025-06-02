# app/models.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SymptomLog(Base):
    __tablename__ = 'symptom_log'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(50), nullable=False)
    CreateDate = Column(Date, nullable=False)
