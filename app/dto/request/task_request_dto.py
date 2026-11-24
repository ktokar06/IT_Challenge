from fastapi import UploadFile
from pydantic import BaseModel

class TaskRequestDTO(BaseModel):
    file: UploadFile
    column: str