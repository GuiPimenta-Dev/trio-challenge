from src.application.usecases.view_menu import ViewMenu
from src.domain.entities.product import Product
from src.infra.repositories.products import InMemoryProductsRepository


def test_it_should_be_able_to_list_all_products():
    products_repository = InMemoryProductsRepository()
    products_repository.add(Product("Latte", ["Pumpkin Spice", "Vanilla", "Hazelnut"]))
    products_repository.add(Product("Cappuccino", ["Caramel", "Vanilla", "Hazelnut"]))
    products_repository.add(Product("Espresso", ["Caramel", "Vanilla", "Hazelnut"]))

    view_menu = ViewMenu(products_repository)

    assert view_menu.execute() == [
        {"name": "Latte", "variations": ["Pumpkin Spice", "Vanilla", "Hazelnut"]},
        {"name": "Cappuccino", "variations": ["Caramel", "Vanilla", "Hazelnut"]},
        {"name": "Espresso", "variations": ["Caramel", "Vanilla", "Hazelnut"]},
    ]
