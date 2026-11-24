from pydantic import BaseModel, ConfigDict

from app.dto.response.statistics_response_dto import StatisticsResponseDTO

class TaskResponseDTO(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: str
    column: str
    result: StatisticsResponseDTO | None = None
    error: str | None = None