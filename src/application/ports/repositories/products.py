from abc import ABC, abstractmethod

from src.domain.entities.product import Product


class ProductsRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        raise NotImplementedError

    @abstractmethod
    def list_all(self):
        raise NotImplementedError
