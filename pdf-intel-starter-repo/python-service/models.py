from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    id: str
    snippet: str


class HealthResponse(BaseModel):
    status: str = "ok"
