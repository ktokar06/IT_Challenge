from pydantic import BaseModel

class ErrorResponseDTO(BaseModel):
    error: str