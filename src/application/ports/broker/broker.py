from abc import ABC, abstractmethod

from src.application.handlers import Handler
from src.domain.events import Event


class Broker(ABC):
    @abstractmethod
    def publish(self, event: Event) -> None:
        pass

    @abstractmethod
    def subscribe(self, handler: Handler) -> None:
        pass
