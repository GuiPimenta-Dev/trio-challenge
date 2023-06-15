import pytest

from src.application.usecases.update_order import UpdateOrder
from src.domain.entities.customer import Customer
from src.domain.entities.product import Product
from src.infra.repositories.customers import InMemoryCustomersRepository
from src.infra.repositories.orders import InMemoryOrdersRepository
from src.infra.repositories.products import InMemoryProductsRepository
from tests.utils.builders.order import OrderBuilder


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


def test_if_is_customer_is_able_to_update_order(repositories):
    products_repository, orders_repository, _ = repositories.values()
    latte = products_repository.find_by_name("Latte")
    latte.choose_variation("Vanilla")
    order = (
        OrderBuilder()
        .with_status("waiting")
        .with_customer_id("default")
        .with_product(latte)
        .build()
    )
    orders_repository.add(order)

    order = {
        "order_id": order.id,
        "customer_id": "default",
        "products": [
            {
                "name": "Latte",
                "variation": "Hazelnut",
            }
        ],
    }
    update_order = UpdateOrder(repositories)
    update_order.execute(order)

    order = orders_repository.find_by_id(order["order_id"])
    assert order.products[0].variation == "Hazelnut"
    assert len(order.products) == 1


def test_error_is_raised_if_customer_not_found(repositories):
    order = {
        "order_id": "order-id",
        "customer_id": "invalid-customer-id",
        "products": [],
    }
    update_order = UpdateOrder(repositories)

    with pytest.raises(Exception) as excinfo:
        update_order.execute(order)

    assert "Customer not found" in str(excinfo.value)


def test_error_is_raised_if_order_not_found(repositories):
    order = {
        "order_id": "some-order-id",
        "customer_id": "default",
        "products": [],
    }
    update_order = UpdateOrder(repositories)

    with pytest.raises(Exception) as excinfo:
        update_order.execute(order)

    assert "Order must have at least one product" in str(excinfo.value)


def test_error_is_raised_if_order_not_found(repositories):
    products_repository, _, _ = repositories.values()
    latte = products_repository.find_by_name("Latte")
    order = {
        "order_id": "invalid-order-id",
        "customer_id": "default",
        "products": [latte],
    }
    update_order = UpdateOrder(repositories)

    with pytest.raises(Exception) as excinfo:
        update_order.execute(order)

    assert "Order not found" in str(excinfo.value)


def test_an_error_should_be_raised_if_customer_is_not_the_same_from_order(repositories):
    products_repository, orders_repository, customers_repository = repositories.values()
    customer = Customer("customer-id", "client@test.com")
    customers_repository.add(customer)
    order = OrderBuilder().build()
    orders_repository.add(order)

    latte = products_repository.find_by_name("Latte")
    order = {
        "order_id": order.id,
        "customer_id": "customer-id",
        "products": [latte],
    }
    update_order = UpdateOrder(repositories)

    with pytest.raises(Exception) as excinfo:
        update_order.execute(order)

    assert "Customer not allowed to update this order" in str(excinfo.value)


def test_should_raise_an_error_if_order_is_not_waiting(repositories):
    products_repository, orders_repository, customers_repository = repositories.values()
    order = OrderBuilder().with_status("ready").build()
    orders_repository.add(order)

    latte = products_repository.find_by_name("Latte")
    order = {
        "order_id": order.id,
        "customer_id": "default",
        "products": [latte],
    }
    update_order = UpdateOrder(repositories)

    with pytest.raises(Exception) as excinfo:
        update_order.execute(order)

    assert "Order cannot be updated with a status different than Waiting" in str(
        excinfo.value
    )


def test_if_location_is_the_same_as_previous_order_if_its_not_sent(repositories):
    _, orders_repository, _ = repositories.values()
    order = OrderBuilder().build()
    orders_repository.add(order)
    old_location = order.location

    order = {
        "order_id": order.id,
        "customer_id": "default",
        "products": [
            {
                "name": "Latte",
            }
        ],
    }
    update_order = UpdateOrder(repositories)
    update_order.execute(order)

    new_order = orders_repository.find_by_id(order["order_id"])
    assert new_order.location == old_location


def test_if_an_order_is_updated_with_a_different_location_if_its_sent(repositories):
    _, orders_repository, _ = repositories.values()
    order = OrderBuilder().build()
    orders_repository.add(order)

    order = {
        "order_id": order.id,
        "customer_id": "default",
        "products": [
            {
                "name": "Latte",
            }
        ],
        "location": "take-away",
    }
    update_order = UpdateOrder(repositories)
    update_order.execute(order)

    new_order = orders_repository.find_by_id(order["order_id"])
    assert new_order.location == "take-away"


def test_if_an_error_is_raised_with_an_invalid_location(repositories):
    _, orders_repository, _ = repositories.values()
    order = OrderBuilder().build()
    orders_repository.add(order)

    order = {
        "order_id": order.id,
        "customer_id": "default",
        "products": [
            {
                "name": "Latte",
            }
        ],
        "location": "invalid-location",
    }
    update_order = UpdateOrder(repositories)
    with pytest.raises(Exception) as excinfo:
        update_order.execute(order)

    assert "Invalid location" in str(excinfo.value)
