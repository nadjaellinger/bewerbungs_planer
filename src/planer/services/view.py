from nicegui import ui
from logging import Logger
from datetime import date

from planer.models.user import User
from planer.models.application import Application
from planer.models.server_settings import ServerSettings
from planer.enums.application_status import ApplicationStatus
from planer.ui.overview import Overview

class View:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.register_landing_page()
        
    def run(self, server_settings: ServerSettings):
        self.logger.info("Starting the application")
        ui.run(
            host=server_settings.server,
            port=server_settings.port,
            title="Bewerbungsplaner",
            reload= False
        )
    
    def register_landing_page(self):
        @ui.page("/")
        def home():
            Overview(self.logger).render(applications=self.fake_applications())
            
    def fake_applications(self):
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
                requires_motivation_letter=False
            ),
            Application(
                id=2,
                company="Company B",
                position="Data Scientist",
                url=None,
                status=ApplicationStatus.INTERVIEWED_FIRST,
                source=None,
                history=[(date(2024, 1, 5), ApplicationStatus.APPLIED), (date(2024, 1, 10), ApplicationStatus.INTERVIEWED_FIRST)],
                comments=None,
                requires_motivation_letter=True
            )
        ]