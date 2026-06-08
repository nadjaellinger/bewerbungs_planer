from pydantic import BaseModel, field_validator

class Application(BaseModel):
    company: str
    position: str
    status: str

