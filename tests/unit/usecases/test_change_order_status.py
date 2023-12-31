import pytest

from src.application.handlers.status_changed import StatusChangedHandler
from src.application.usecases.change_order_status import ChangeOrderStatus
from src.infra.broker.broker import InMemoryBroker
from src.infra.repositories.customers import InMemoryCustomersRepository
from src.infra.repositories.managers import InMemoryManagersRepository
from src.infra.repositories.orders import InMemoryOrdersRepository
from tests.utils.builders.order import OrderBuilder
from tests.utils.mocks.mailer_spy import MailerSpy


def test_a_manager_should_be_able_to_change_an_order_status():
    managers_repository = InMemoryManagersRepository()
    orders_repository = InMemoryOrdersRepository()
    broker = InMemoryBroker()
    managers_repository.create_default_manager()
    order = OrderBuilder().with_status("waiting").build()
    orders_repository.add(order)

    change_order_status = ChangeOrderStatus(
        managers_repository, orders_repository, broker
    )
    input_dto = {"order_id": order.id, "manager_id": "manager-id"}
    change_order_status.execute(input_dto)

    order = orders_repository.find_by_id(order.id)
    assert order.status == "Preparation"


def test_a_non_manager_should_not_be_able_to_change_an_order_status():
    managers_repository = InMemoryManagersRepository()
    orders_repository = InMemoryOrdersRepository()
    broker = InMemoryBroker()
    order = OrderBuilder().with_status("waiting").build()
    orders_repository.add(order)

    change_order_status = ChangeOrderStatus(
        managers_repository, orders_repository, broker
    )
    input_dto = {"order_id": order.id, "manager_id": "manager-id"}
    with pytest.raises(Exception) as excinfo:
        change_order_status.execute(input_dto)

    assert str(excinfo.value) == "You must be a manager to perform this action"


def test_a_manager_should_not_be_able_to_change_the_status_of_a_non_existing_order():
    managers_repository = InMemoryManagersRepository()
    orders_repository = InMemoryOrdersRepository()
    broker = InMemoryBroker()
    managers_repository.create_default_manager()

    change_order_status = ChangeOrderStatus(
        managers_repository, orders_repository, broker
    )
    input_dto = {"order_id": 1, "manager_id": "manager-id"}
    with pytest.raises(Exception) as excinfo:
        change_order_status.execute(input_dto)

    assert str(excinfo.value) == "Order not found"


def test_if_an_email_is_sent_after_every_order_status_change():
    managers_repository = InMemoryManagersRepository()
    orders_repository = InMemoryOrdersRepository()
    customers_repository = InMemoryCustomersRepository()
    customers_repository.create_default_customer()
    broker = InMemoryBroker()
    mailer_spy = MailerSpy()
    status_changed_handler = StatusChangedHandler(mailer_spy, customers_repository)
    broker.subscribe(status_changed_handler)
    order = OrderBuilder().with_status("waiting").build()
    managers_repository.create_default_manager()

    orders_repository.add(order)

    change_order_status = ChangeOrderStatus(
        managers_repository, orders_repository, broker
    )
    input_dto = {"order_id": order.id, "manager_id": "manager-id"}
    change_order_status.execute(input_dto)
    change_order_status.execute(input_dto)
    change_order_status.execute(input_dto)

    assert len(mailer_spy.emails) == 3
    assert mailer_spy.emails[0]["body"] == "Order status changed to Preparation"
    assert mailer_spy.emails[1]["body"] == "Order status changed to Ready"
    assert mailer_spy.emails[2]["body"] == "Order status changed to Delivered"


def test_if_an_exception_is_raised_case_order_is_already_delivered():
    managers_repository = InMemoryManagersRepository()
    orders_repository = InMemoryOrdersRepository()
    broker = InMemoryBroker()
    order = OrderBuilder().with_status("delivered").build()
    managers_repository.create_default_manager()
    orders_repository.add(order)

    change_order_status = ChangeOrderStatus(
        managers_repository, orders_repository, broker
    )
    input_dto = {"order_id": order.id, "manager_id": "manager-id"}
    with pytest.raises(Exception) as excinfo:
        change_order_status.execute(input_dto)

    assert str(excinfo.value) == "Order already delivered"
