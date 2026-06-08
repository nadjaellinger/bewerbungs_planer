from fastapi import APIRouter
from datetime import date

from planer.models.application import Application
from planer.enums.application_status import ApplicationStatus

router = APIRouter(prefix="/applications", tags=["applications"])


def _fake_applications() -> list[Application]:
    return [
        Application(
            id=1,
            company="Company A",
            position="Software Engineer",
            url="https://companya.com/careers/123",
            status=ApplicationStatus.APPLIED,
            source="LinkedIn",
            history=[(date(2024, 1, 1), ApplicationStatus.APPLIED)],
            comments="Applied via LinkedIn.",
            requires_motivation_letter=False,
        ),
        Application(
            id=2,
            company="Company B",
            position="Data Scientist",
            url=None,
            status=ApplicationStatus.INTERVIEWED_FIRST,
            source=None,
            history=[
                (date(2024, 1, 5), ApplicationStatus.APPLIED),
                (date(2024, 1, 10), ApplicationStatus.INTERVIEWED_FIRST),
            ],
            comments=None,
            requires_motivation_letter=True,
        ),
        Application(
            id=3,
            company="Company C",
            position="Backend Developer",
            url="https://companyc.io/jobs/42",
            status=ApplicationStatus.OFFERED,
            source="Xing",
            history=[
                (date(2024, 2, 1), ApplicationStatus.APPLIED),
                (date(2024, 2, 10), ApplicationStatus.INVITED_FIRST),
                (date(2024, 2, 20), ApplicationStatus.OFFERED),
            ],
            comments="Sehr gutes Gespräch.",
            requires_motivation_letter=False,
        ),
    ]


@router.get("/", response_model=list[Application])
def list_applications() -> list[Application]:
    return _fake_applications()
