from abc import ABC, abstractmethod

from src.domain.events import Event


class Handler(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def handle(self, event: Event) -> None:
        pass
