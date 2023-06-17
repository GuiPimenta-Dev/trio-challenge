from src.application.usecases.view_menu import ViewMenu
from src.domain.entities.product import Product
from src.infra.repositories.products import InMemoryProductsRepository


def test_it_should_be_able_to_list_all_products():
    products_repository = InMemoryProductsRepository()

    view_menu = ViewMenu(products_repository)

    assert view_menu.execute() == [
        {"name": "Latte", "variations": ["Pumpkin Spice", "Vanilla", "Hazelnut"]},
        {"name": "Cappuccino", "variations": ["Small", "Medium", "Large"]},
        {
            "name": "Iced Drinks",
            "variations": ["Smoothie", "Iced Coffee", "Iced Macchiato"],
        },
        {"name": "Tea", "variations": []},
        {"name": "Hot Chocolate", "variations": ["Small", "Medium", "Large"]},
        {"name": "Donuts", "variations": ["Glazed", "Jelly", "Boston Cream"]},
    ]
