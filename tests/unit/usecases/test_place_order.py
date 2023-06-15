import pytest

from src.application.usecases.place_order import PlaceOrder
from src.domain.entities.customer import Customer
from src.infra.repositories.customers import InMemoryCustomersRepository
from src.infra.repositories.orders import InMemoryOrdersRepository
from src.infra.repositories.products import InMemoryProductsRepository


@pytest.fixture
def repositories():
    products_repository = InMemoryProductsRepository()
    orders_repository = InMemoryOrdersRepository()
    customers_repository = InMemoryCustomersRepository()
    customers_repository.add(Customer("id", "customer@test.com"))

    yield {
        "products_repository": products_repository,
        "orders_repository": orders_repository,
        "customers_repository": customers_repository,
    }


def test_order_is_successfuly_created_in_orders_repository(repositories):
    order = {
        "customer_id": "id",
        "products": [
            {
                "name": "Latte",
                "variation": "Vanilla",
            },
            {
                "name": "Cappuccino",
                "variation": "Small",
            },
        ],
    }
    place_order = PlaceOrder(repositories)

    place_order.execute(order)

    order = repositories["orders_repository"].list_all()[0]

    assert order.id is not None
    assert order.customer_id == "id"
    assert len(order.products) == 2
    assert order.status.value == "waiting"


def test_error_is_raised_if_customer_is_not_found(repositories):
    order = {
        "customer_id": "invalid_id",
        "products": [
            {
                "name": "Latte",
                "variation": "Vanilla",
            },
            {
                "name": "Cappuccino",
                "variation": "Small",
            },
        ],
    }
    place_order = PlaceOrder(repositories)

    with pytest.raises(ValueError) as excinfo:
        place_order.execute(order)

    assert "Customer not found" in str(excinfo.value)


def test_error_is_raised_if_order_does_not_have_products(repositories):
    order = {
        "customer_id": "id",
        "products": [],
    }
    place_order = PlaceOrder(repositories)

    with pytest.raises(ValueError) as excinfo:
        place_order.execute(order)

    assert "Order must have at least one product" in str(excinfo.value)


def test_error_is_raised_if_product_is_not_found(repositories):
    order = {
        "customer_id": "id",
        "products": [
            {
                "name": "invalid_product",
                "variation": "Vanilla",
            },
        ],
    }
    place_order = PlaceOrder(repositories)

    with pytest.raises(ValueError) as excinfo:
        place_order.execute(order)

    assert "Invalid product" in str(excinfo.value)


def test_error_is_raised_if_product_variation_is_not_found(repositories):
    order = {
        "customer_id": "id",
        "products": [
            {
                "name": "Latte",
                "variation": "invalid_variation",
            },
        ],
    }
    place_order = PlaceOrder(repositories)

    with pytest.raises(ValueError) as excinfo:
        place_order.execute(order)

    assert "Invalid variation" in str(excinfo.value)


def test_if_variation_is_saved_as_expected_on_the_database(repositories):
    order = {
        "customer_id": "id",
        "products": [
            {
                "name": "Latte",
                "variation": "Vanilla",
            },
            {
                "name": "Latte",
            },
        ],
    }
    place_order = PlaceOrder(repositories)

    place_order.execute(order)

    order = repositories["orders_repository"].list_all()[0]

    assert order.products[0].variation == "Vanilla"
    assert order.products[1].variation is None
