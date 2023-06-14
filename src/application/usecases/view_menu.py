from . import UseCase


class ViewMenu(UseCase):
    def __init__(self, products_repository):
        self.products_repository = products_repository

    def execute(self):
        all_products = self.products_repository.list_all()
        return [
            {"name": product.name, "variations": product.variations}
            for product in all_products
        ]
