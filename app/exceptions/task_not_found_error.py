from app.constants import messages

class TaskNotFoundError(Exception):
    """Задание с указанным id не найдено: ответ 404."""

    def __init__(self, task_id):
        self.task_id = task_id
        super().__init__(messages.TASK_NOT_FOUND.format(task_id=task_id))