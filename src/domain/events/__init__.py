from abc import ABC, abstractmethod


class Event(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass
