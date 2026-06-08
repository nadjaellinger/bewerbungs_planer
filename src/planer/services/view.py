from nicegui import ui
from logging import Logger

from planer.models.user import User
from planer.models.application import Application

class View:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.register_landing_page()
        
    def run(self, server_settings):
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
            ui.label("Willkommen zum Bewerbungsplaner!")