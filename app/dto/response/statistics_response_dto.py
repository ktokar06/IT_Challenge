from pydantic import BaseModel

class StatisticsResponseDTO(BaseModel):
    count: int
    min: float
    max: float
    mean: float