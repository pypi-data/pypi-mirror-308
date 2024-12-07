import logging
import os
from datetime import datetime

class CustomLogger:
    _instance = None
    def __new__(cls, name: str = __name__):
        if cls._instance is None:
            cls._instance = super(CustomLogger, cls).__new__(cls)
            cls._instance.logger = logging.getLogger(name)

            # Créer un fichier de log avec l'heure actuelle comme nom
            log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log")
            log_directory = "logs"
            if not os.path.exists(log_directory):
                os.makedirs(log_directory)
            file_handler = logging.FileHandler(os.path.join(log_directory, log_filename))
            stream_handler = logging.StreamHandler()

            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)

            cls._instance.logger.addHandler(file_handler)
            cls._instance.logger.addHandler(stream_handler)
            cls._instance.logger.setLevel(logging.DEBUG)
        return cls._instance

    def debug(self, message: str):
        self.logger.debug(message)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def critical(self, message: str):
        self.logger.critical(message)