from . import models
from . import crud
import importlib.util
import time
import os
from multiprocessing import Process
import site
#from features import heartrate import run_video
from .features.heartrate import NoGUI

def main_process(db):
    while True:
        next_task = crud.get_next_task(db)
        if next_task != None :
            run_task(db, next_task)
        else:
            print('no task, sleep 1')
            time.sleep(1)
    
def start_process(db: crud.DBSession):
    p = Process(target=main_process, args=(db,))
    p.start()

def run_task(db: crud.DBSession, task: models.Task):    
    
    print("update status to processing taskid :" + task.id)
    crud.update_status(db, task.id, "processing")

    #site.addsitedir('../heartrate')  # Always appends to end

    #spec = importlib.util.spec_from_file_location("module.name", "../heartrate/NoGUI.py")
    #foo = importlib.util.module_from_spec(spec)
    #spec.loader.exec_module(foo)
    #foo.run_video(task.filepath)
    result = NoGUI.run_video(task.id)
    
    print("start result" + result)
    # os.system('python ../heartrate/NoGUI.py ' + task.filepath)
    
    print("finish task" + task.id)
    crud.update_status(db, task.id, "completed", result)