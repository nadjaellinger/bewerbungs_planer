import logging
from dotenv import load_dotenv
import os
import uvicorn

from planer.models.server_settings import ServerSettings

class App:
    def __init__(self):
        self.logger = self.get_logger()
        self.server_settings = self.get_server_settings()

    def run(self):
        uvicorn.run(
            "planer.api.main:app",
            host=self.server_settings.server,
            port=self.server_settings.port,
            reload=True,
        )
        
    def get_logger(self) -> logging.Logger:
        logger = logging.getLogger("planer")
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger
    
    def get_server_settings(self):
        #load from .env
        try:
            load_dotenv()
            server = os.getenv("SERVER", "localhost")
            port = int(os.getenv("PORT", "8000"))
            return ServerSettings(server=server, port=port)
        except Exception as e:
            self.logger.error(f"Error loading server settings: {e}")
            return ServerSettings(server="localhost", port=8000)