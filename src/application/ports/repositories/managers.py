from abc import ABC, abstractmethod

from src.domain.entities.manager import Manager


class ManagersRepository(ABC):
    @abstractmethod
    def add(self, manager: Manager):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Manager:
        raise NotImplementedError
