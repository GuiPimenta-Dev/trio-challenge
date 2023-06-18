from src.application.errors import HttpException
from src.application.ports.repositories.products import ProductsRepository
from src.domain.entities.product import Product
from src.domain.service.products import ProductsService
from src.infra.repositories.products import InMemoryProductsRepository

products_repository = InMemoryProductsRepository()
products_service = ProductsService(products_repository)


def test_it_should_get_a_list_of_products():
    products_dto = [{"name": "Latte"}]
    products = products_service.get_products(products_dto)

    assert isinstance(products[0], Product)


def test_it_should_choose_a_variation():
    products_dto = [{"name": "Latte", "variation": "Vanilla"}]
    products = products_service.get_products(products_dto)

    assert products[0].variation == "Vanilla"


def test_it_should_raise_an_error_if_there_is_no_products():
    products_dto = []
    try:
        products_service.get_products(products_dto)
    except HttpException as error:
        assert str(error) == "There must be at least one product"


def test_it_should_raise_an_error_if_product_is_not_found():
    products_dto = [{"name": "invalid_product"}]
    try:
        products_service.get_products(products_dto)
    except HttpException as error:
        assert str(error) == "Invalid product"
