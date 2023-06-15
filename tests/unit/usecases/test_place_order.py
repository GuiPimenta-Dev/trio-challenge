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
    customers_repository.create_default_customer()

    yield {
        "products_repository": products_repository,
        "orders_repository": orders_repository,
        "customers_repository": customers_repository,
    }


def test_order_is_successfuly_created_in_orders_repository(repositories):
    order = {
        "customer_id": "default",
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
    assert order.customer_id == "default"
    assert len(order.products) == 2
    assert order.status == "Waiting"


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


def test_error_is_raised_if_product_is_not_found(repositories):
    order = {
        "customer_id": "default",
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
        "customer_id": "default",
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
        "customer_id": "default",
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


def test_if_order_is_placed_with_take_away_location(repositories):
    order = {
        "customer_id": "default",
        "products": [
            {
                "name": "Latte",
                "variation": "Vanilla",
            },
            {
                "name": "Latte",
            },
        ],
        "location": "take-away",
    }
    place_order = PlaceOrder(repositories)

    place_order.execute(order)

    order = repositories["orders_repository"].list_all()[0]
    assert order.location == "take-away"


def test_if_an_error_is_raised_if_location_is_invalid(repositories):
    order = {
        "customer_id": "default",
        "products": [
            {
                "name": "Latte",
                "variation": "Vanilla",
            },
            {
                "name": "Latte",
            },
        ],
        "location": "invalid-location",
    }
    place_order = PlaceOrder(repositories)
    with pytest.raises(ValueError) as excinfo:
        place_order.execute(order)

    assert "Invalid location" in str(excinfo.value)


def test_if_default_location_is_in_house(repositories):
    order = {
        "customer_id": "default",
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
    assert order.location == "in-house"
