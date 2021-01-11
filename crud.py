from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
import models

import uuid
from datetime import datetime

SQLALCHEMY_DATABASE_URL = 'sqlite:///tasks.db' #os.environ['SQLALCHEMY_DATABASE_URL']
engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
#session = DBSession()

def create_task(db: DBSession, filepath: str):
    uid =  uuid.uuid4().hex
    task = models.Task(id = uid, filepath = filepath, status = 'created', completed=False)
    history = models.History(id = uid, time = datetime.now(), task = task)
    db.add(task)
    db.commit()
    db.add(history)
    db.commit()
    return task

def update_status(db: DBSession, task_id: str, task_status: str):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    task.status = status
    if task_status == "completed":
        task.completed = True
    db.commit()

    history = models.History(id = uid, time = datetime(), task = task)
    db.add(history)
    db.commit()

def get_task(db: DBSession, task_id: str):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    return task
    
def get_task_history(db: DBSession, userid: int):
   return db.query(models.History).filter(models.TODO.owner_id == userid).all()