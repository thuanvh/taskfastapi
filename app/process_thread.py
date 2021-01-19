from . import models
from . import crud
import importlib.util
import time
import os

from threading import Thread, Event
#from multiprocessing import Process, Event

import site
#from features import heartrate import run_video
from .features.heartrate import NoGUI
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
 
from . import models

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

event = Event()
task_list = []
db = None
_process = None
_stop = False

def add_task(task):
    task_list.append(task)

def main_process():
    db = crud.DBSession()
    while not _stop:
        next_task = crud.get_next_task(db)
        if next_task != None :
            run_task(db, next_task)
        else:
            print('no task, sleep 1')
            time.sleep(2)
        if event.is_set():
            break
    print('stop process')
    db.close()
    
def start_process():
    #_process = Process(target=main_process)
    #_process.start()
    _process = Thread(target=main_process)
    _process.start()

def end_process():
    print("stop to true")
    _stop = True
    event.set()
    print("try stop process")
    #_process.terminate()

def run_task(db: crud.DBSession, task: models.Task):    
    
    print("update status to processing taskid :" + task.id)
    crud.update_status(db, task.id, "processing")

    #site.addsitedir('../heartrate')  # Always appends to end

    #spec = importlib.util.spec_from_file_location("module.name", "../heartrate/NoGUI.py")
    #foo = importlib.util.module_from_spec(spec)
    #spec.loader.exec_module(foo)
    #foo.run_video(task.filepath)
    
    result = NoGUI.run_video(task.id)
    #time.sleep(1)
    #result = str({ "test" : 1000})
    
    print("start result" + result)
    # os.system('python ../heartrate/NoGUI.py ' + task.filepath)
    
    print("finish task" + task.id)
    crud.update_status(db, task.id, "completed", result)