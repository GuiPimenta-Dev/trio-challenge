import pytest

from src.application.usecases.cancel_order import CancelOrder
from src.domain.entities.customer import Customer
from src.infra.repositories.customers import InMemoryCustomersRepository
from src.infra.repositories.orders import InMemoryOrdersRepository
from tests.utils.builders.order import OrderBuilder


def test_it_should_cancel_an_order():
    customers_repository = InMemoryCustomersRepository()
    orders_repository = InMemoryOrdersRepository()
    customers_repository.create_default_customer()
    order = OrderBuilder().build()
    orders_repository.add(order)

    cancel_order = CancelOrder(customers_repository, orders_repository)
    cancel_order.execute(order.id, "default")

    order = orders_repository.find_by_id(order.id)
    assert order is None


def test_it_should_not_cancel_an_order_if_customer_not_found():
    customers_repository = InMemoryCustomersRepository()
    orders_repository = InMemoryOrdersRepository()

    cancel_order = CancelOrder(customers_repository, orders_repository)
    with pytest.raises(Exception) as excinfo:
        cancel_order.execute("1", "default")

    assert str(excinfo.value) == "Customer not found"


def test_it_should_raise_error_if_order_not_found():
    customers_repository = InMemoryCustomersRepository()
    orders_repository = InMemoryOrdersRepository()
    customers_repository.create_default_customer()

    cancel_order = CancelOrder(customers_repository, orders_repository)
    with pytest.raises(Exception) as excinfo:
        cancel_order.execute("1", "default")

    assert str(excinfo.value) == "Order not found"


def test_it_should_raise_error_if_customer_is_different_then_customer_id_in_order():
    customers_repository = InMemoryCustomersRepository()
    orders_repository = InMemoryOrdersRepository()
    customers_repository.create_default_customer()
    customer = Customer("customer-id", "test@test.com")
    customers_repository.add(customer)
    order = OrderBuilder().build()
    orders_repository.add(order)

    cancel_order = CancelOrder(customers_repository, orders_repository)
    with pytest.raises(Exception) as excinfo:
        cancel_order.execute(order.id, "customer-id")

    assert str(excinfo.value) == "Order does not belong to this customer"


def test_it_should_not_cancel_if_status_is_not_waiting():
    customers_repository = InMemoryCustomersRepository()
    orders_repository = InMemoryOrdersRepository()
    customers_repository.create_default_customer()
    order = OrderBuilder().with_status("ready").build()
    orders_repository.add(order)

    cancel_order = CancelOrder(customers_repository, orders_repository)
    with pytest.raises(Exception) as excinfo:
        cancel_order.execute(order.id, "default")

    assert str(excinfo.value) == "Order must be in Waiting status to be canceled"
