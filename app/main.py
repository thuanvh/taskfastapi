from fastapi import FastAPI, File, UploadFile

from . import crud
import shutil

app = FastAPI()

session = crud.DBSession()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tasks/{task_id}")
async def read_task(task_id: str):
    task = crud.get_task(session, task_id)
    return {"status": task.status}

@app.post("/uploadfile/")
def create_task(uploaded_file: UploadFile = File(...)):
    file_location = f"files/{uploaded_file.filename}"
    uploaded_file.file.seek(0)  # <-- This.

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(uploaded_file.file, file_object)
    task = crud.create_task(session, file_location)
    #return {"filename": file.filename, "content_type" : file.content_type}
    return {"taskid": task.id}

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