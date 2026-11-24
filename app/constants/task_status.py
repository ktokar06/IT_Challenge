from enum import Enum

class TaskStatus(str, Enum):
    """Статусы задания: pending - processing - completed или failed."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"