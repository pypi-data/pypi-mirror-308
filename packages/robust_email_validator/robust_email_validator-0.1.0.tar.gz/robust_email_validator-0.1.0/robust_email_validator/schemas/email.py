from pydantic import BaseModel


class EmailResponse(BaseModel):
    email: str
    is_valid: bool


class SingleEmailRequest(BaseModel):
    email: str


class BulkEmailRequest(BaseModel):
    email: list[str]
