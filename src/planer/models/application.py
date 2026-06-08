from typing import List, Tuple, Optional
from datetime import date

from pydantic import BaseModel

from planer.enums.application_status import ApplicationStatus

class Application(BaseModel):
    id: int
    company: str
    position: str
    url: Optional[str]
    status: ApplicationStatus
    source: Optional[str]
    history: List[Tuple[date, ApplicationStatus]] = []
    comments: Optional[str]
    requires_motivation_letter: bool = False
    

