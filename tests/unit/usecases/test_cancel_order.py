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

    cancel_order = CancelOrder(orders_repository)
    cancel_order.execute(order.id)

    order = orders_repository.find_by_id(order.id)
    assert order is None


def test_it_should_raise_error_if_order_not_found():
    orders_repository = InMemoryOrdersRepository()

    cancel_order = CancelOrder(orders_repository)
    with pytest.raises(Exception) as excinfo:
        cancel_order.execute("1")

    assert str(excinfo.value) == "Order not found"


def test_it_should_not_cancel_if_status_is_not_waiting():
    orders_repository = InMemoryOrdersRepository()
    order = OrderBuilder().with_status("ready").build()
    orders_repository.add(order)

    cancel_order = CancelOrder(orders_repository)
    with pytest.raises(Exception) as excinfo:
        cancel_order.execute(order.id)

    assert str(excinfo.value) == "Order must be in Waiting status to be canceled"
