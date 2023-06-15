from abc import ABC, abstractmethod


class OrdersRepository(ABC):
    @abstractmethod
    def add(self):
        raise NotImplementedError

    @abstractmethod
    def list_all(self):
        raise NotImplementedError
