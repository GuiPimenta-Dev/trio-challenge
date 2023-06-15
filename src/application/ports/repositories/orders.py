from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.order import Order


class OrdersRepository(ABC):
    @abstractmethod
    def add(self, order: Order):
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Order]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, order_id: str) -> Order:
        raise NotImplementedError

    @abstractmethod
    def update(self, order: Order) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, order_id: str) -> None:
        raise NotImplementedError
