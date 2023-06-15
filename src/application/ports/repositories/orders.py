from abc import ABC, abstractmethod


class OrdersRepository(ABC):
    @abstractmethod
    def add(self):
        raise NotImplementedError

    @abstractmethod
    def list_all(self):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError
