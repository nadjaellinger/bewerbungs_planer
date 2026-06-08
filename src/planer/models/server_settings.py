from pydantic import BaseModel

class ServerSettings(BaseModel):
    server: str
    port: int