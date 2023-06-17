from copy import deepcopy
from typing import List

from src.application.ports.repositories.products import ProductsRepository
from src.domain.entities.product import Product


class InMemoryProductsRepository(ProductsRepository):
    def __init__(self):
        self.products = [
            Product("Latte", ["Pumpkin Spice", "Vanilla", "Hazelnut"]),
            Product("Cappuccino", ["Small", "Medium", "Large"]),
            Product("Iced Drinks", ["Smoothie", "Iced Coffee", "Iced Macchiato"]),
            Product("Tea", []),
            Product("Hot Chocolate", ["Small", "Medium", "Large"]),
            Product("Donuts", ["Glazed", "Jelly", "Boston Cream"]),
        ]

    def add(self, product: Product):
        self.products.append(product)

    def find_by_name(self, name: str) -> Product:
        product = next(
            (product for product in self.products if product.name == name), None
        )
        return deepcopy(product)

    def list_all(self) -> List[Product]:
        return self.products
