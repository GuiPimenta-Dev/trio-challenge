from src.application.ports.repositories.products import ProductsRepository


class InMemoryProductsRepository(ProductsRepository):
    def __init__(self):
        self.products = []

    def add(self, product):
        self.products.append(product)

    def list_all(self):
        return self.products
