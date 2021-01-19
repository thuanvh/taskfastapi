from fastapi import FastAPI, File, UploadFile

from . import crud
import shutil

from .process_thread import start_process, end_process
import os
import uuid

app = FastAPI()

db = crud.DBSession()

@app.on_event("startup")
async def startup_event():
    start_process()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tasks/{task_id}")
async def read_task(task_id: str):
    db = crud.DBSession()
    task = crud.get_task(db, task_id)
    return {"status": task.status, "result": task.result}

@app.post("/uploadfile/")
def create_task(uploaded_file: UploadFile = File(...)):
    db = crud.DBSession()
    if not os.path.exists("files"):
        os.makedirs("files")
    ext_list = (uploaded_file.filename).split('.')

    ext = ext_list[1] if len(ext_list) > 1 else ""
    uid =  uuid.uuid4().hex
    file_location = f"files/{uid}.{ext}"
    uploaded_file.file.seek(0)  # <-- This.

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object)
    task = crud.create_task(db, file_location)
    #return {"filename": file.filename, "content_type" : file.content_type}
    return {"taskid": task.id}

@app.on_event("shutdown")
def shutdown_event():
    print("shutdown event")
    end_process()
    sys.exit()
# import shutil
# from pathlib import Path
# from tempfile import NamedTemporaryFile
# from typing import Callable

# from fastapi import UploadFile


# def save_upload_file(upload_file: UploadFile, destination: Path) -> None:
#     try:
#         with destination.open("wb") as buffer:
#             shutil.copyfileobj(upload_file.file, buffer)
#     finally:
#         upload_file.file.close()


# def save_upload_file_tmp(upload_file: UploadFile) -> Path:
#     try:
#         suffix = Path(upload_file.filename).suffix
#         with NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
#             shutil.copyfileobj(upload_file.file, tmp)
#             tmp_path = Path(tmp.name)
#     finally:
#         upload_file.file.close()
#     return tmp_path


# def handle_upload_file(
#     upload_file: UploadFile, handler: Callable[[Path], None]
# ) -> None:
#     tmp_path = save_upload_file_tmp(upload_file)
#     try:
#         handler(tmp_path)  # Do something with the saved temp file
#     finally:
#         tmp_path.unlink()  # Delete the temp file