from typing import Annotated

from fastapi import APIRouter, Depends, File, status
from sqlalchemy.orm import Session

from app.constants import messages
from app.database import get_db
from app.dto.request.task_request_dto import TaskRequestDTO
from app.dto.response.error_response_dto import ErrorResponseDTO
from app.dto.response.health_response_dto import HealthResponseDTO
from app.dto.response.task_response_dto import TaskResponseDTO
from app.exceptions.statistics_error import StatisticsError
from app.services import task_service
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

ERROR_RESPONSE = {"model": ErrorResponseDTO}

@router.get("/health", status_code=status.HTTP_200_OK, response_model=HealthResponseDTO)
def health() -> HealthResponseDTO:
    return HealthResponseDTO(status="ok")

@router.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=TaskResponseDTO,
             responses={status.HTTP_400_BAD_REQUEST: ERROR_RESPONSE, status.HTTP_422_UNPROCESSABLE_CONTENT: ERROR_RESPONSE})
def create_task(request: Annotated[TaskRequestDTO, File()], db: Session = Depends(get_db)) -> TaskResponseDTO:
    logger.info("POST /tasks: файл '%s', столбец '%s'", request.file.filename, request.column)
    try:
        content = request.file.file.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        raise StatisticsError(messages.INVALID_ENCODING)
    task = task_service.create_task(db, request.column, content)
    task = task_service.process_task(db, task)
    return TaskResponseDTO.model_validate(task)

@router.get("/tasks", status_code=status.HTTP_200_OK, response_model=list[TaskResponseDTO])
def list_tasks(db: Session = Depends(get_db)) -> list[TaskResponseDTO]:
    return [TaskResponseDTO.model_validate(task) for task in task_service.get_tasks(db)]

@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK, response_model=TaskResponseDTO,
            responses={status.HTTP_404_NOT_FOUND: ERROR_RESPONSE, status.HTTP_422_UNPROCESSABLE_CONTENT: ERROR_RESPONSE})
def get_task(task_id: int, db: Session = Depends(get_db)) -> TaskResponseDTO:
    task = task_service.get_task(db, task_id)
    return TaskResponseDTO.model_validate(task)