from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.constants import messages
from app.dto.response.error_response_dto import ErrorResponseDTO
from app.exceptions.statistics_error import StatisticsError
from app.exceptions.task_not_found_error import TaskNotFoundError
from app.utils.logger import get_logger

logger = get_logger(__name__)

def error_response(status_code: int, message: str) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=ErrorResponseDTO(error=message).model_dump())

def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return error_response(status.HTTP_404_NOT_FOUND, str(exc))

def bad_file_handler(request: Request, exc: StatisticsError) -> JSONResponse:
    logger.warning("%s %s: %s", request.method, request.url.path, exc)
    return error_response(status.HTTP_400_BAD_REQUEST, str(exc))

def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    details = []
    for error in exc.errors():
        field = error["loc"][-1]
        template = messages.FIELD_REQUIRED if error["type"] == "missing" else messages.FIELD_INVALID
        details.append(template.format(field=field))
    message = messages.VALIDATION_ERROR.format(details=", ".join(details))
    logger.warning("%s %s: %s", request.method, request.url.path, message)
    return error_response(status.HTTP_422_UNPROCESSABLE_CONTENT, message)

def server_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("%s %s: внутренняя ошибка сервера", request.method, request.url.path, exc_info=exc)
    return error_response(status.HTTP_500_INTERNAL_SERVER_ERROR, messages.INTERNAL_ERROR)

def register_handlers(app) -> None:
    app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
    app.add_exception_handler(StatisticsError, bad_file_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(Exception, server_error_handler)