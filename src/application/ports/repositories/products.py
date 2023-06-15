from abc import ABC, abstractmethod
from typing import List

from src.domain.entities.product import Product


class ProductsRepository(ABC):
    @abstractmethod
    def add(self, product: Product):
        raise NotImplementedError

    @abstractmethod
    def find_by_name(self, name: str) -> Product:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> List[Product]:
        raise NotImplementedError
