from sqlalchemy import JSON, Column, Integer, String, Text

from app.constants.task_status import TaskStatus
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column("id", Integer, primary_key=True)
    column = Column("column", String(255), nullable=False)
    status = Column("status", String(20), nullable=False, default=TaskStatus.PENDING.value)
    content = Column("content", Text, nullable=False)
    result = Column("result", JSON)
    error = Column("error", Text)