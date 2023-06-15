from abc import ABC, abstractmethod

from src.domain.entities.customer import Customer


class CustomersRepository(ABC):
    @abstractmethod
    def add(self, customer: Customer):
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: str) -> Customer:
        raise NotImplementedError
