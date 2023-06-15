from copy import deepcopy
from typing import List

from src.application.ports.repositories.products import ProductsRepository
from src.domain.entities.product import Product


class InMemoryProductsRepository(ProductsRepository):
    def __init__(self):
        self.products = []
        self.add(Product("Latte", ["Pumpkin Spice", "Vanilla", "Hazelnut"]))
        self.add(Product("Cappuccino", ["Small", "Medium", "Large"]))
        self.add(Product("Iced Drinks", ["Smoothie", "Iced Coffee", "Iced Macchiato"]))

    def add(self, product: Product):
        self.products.append(product)

    def find_by_name(self, name: str) -> Product:
        product = next(
            (product for product in self.products if product.name == name), None
        )
        return deepcopy(product)

    def list_all(self) -> List[Product]:
        return self.products
