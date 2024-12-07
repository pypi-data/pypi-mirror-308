from src.mqtt_backend_serrawatch.utils import CustomLogger

Logger = CustomLogger()

class TopicsConfig:
    def __init__(self, publisher: str, subscriber: str):
        self.publisher = publisher
        self.subscriber = subscriber
        Logger.debug(f"TopicsConfig initialized with publisher: {publisher}, subscriber: {subscriber}")