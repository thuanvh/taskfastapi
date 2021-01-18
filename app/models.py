import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

SQLALCHEMY_DATABASE_URL = 'sqlite:///tasks.db' #os.environ['SQLALCHEMY_DATABASE_URL']
#SessionLocal = sessionmaker(autocommit=False, autoFlush=False, bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(String, primary_key=True, index=True)
    filepath = Column(String)
    status = Column(String)
    completed = Column(Boolean)
    result = Column(Text)
    histories = relationship("History", back_populates="task", cascade="all, delete-orphan")

class History(Base):
    __tablename__ = "histories"
    id = Column(String, primary_key=True, index=True)
    status = Column(String)
    time = Column(DateTime)
    task_id = Column(String, ForeignKey("tasks.id"))
    task = relationship("Task", back_populates="histories")

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base.metadata.create_all(engine)