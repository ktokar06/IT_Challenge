from sqlalchemy.orm import Session

from app.constants import messages
from app.constants.task_status import TaskStatus
from app.exceptions.statistics_error import StatisticsError
from app.exceptions.task_not_found_error import TaskNotFoundError
from app.models.task import Task
from app.services.statistics import calculate_statistics
from app.utils.logger import get_logger

logger = get_logger(__name__)

def create_task(db: Session, column: str, content: str) -> Task:
    task = Task(column=column, content=content, status=TaskStatus.PENDING.value)
    db.add(task)
    db.commit()
    logger.info("Задание %s создано, столбец '%s'", task.id, column)
    return task

def process_task(db: Session, task: Task) -> Task:
    task.status = TaskStatus.PROCESSING.value
    db.commit()
    logger.info("Задание %s: статус %s", task.id, task.status)
    try:
        task.result = calculate_statistics(task.content, task.column)
        task.status = TaskStatus.COMPLETED.value
        logger.info("Задание %s выполнено: %s", task.id, task.result)
    except StatisticsError as e:
        task.error = str(e)
        task.status = TaskStatus.FAILED.value
        logger.warning("Задание %s: ошибка в данных — %s", task.id, e)
    except Exception:
        task.error = messages.CALCULATION_FAILED
        task.status = TaskStatus.FAILED.value
        logger.exception("Задание %s: непредвиденная ошибка расчета", task.id)
    db.commit()
    return task

def get_task(db: Session, task_id: int) -> Task:
    task = db.get(Task, task_id)
    if task is None:
        logger.warning("Задание %s не найдено", task_id)
        raise TaskNotFoundError(task_id)
    return task

def get_tasks(db: Session) -> list[Task]:
    return db.query(Task).order_by(Task.id).all()