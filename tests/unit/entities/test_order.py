import pytest

from tests.utils.builders.order import OrderBuilder


def test_order_status_value_should_be_waiting():
    order = OrderBuilder().with_status("waiting").build()

    assert order._status.value == "Waiting"


def test_order_status_value_should_be_preparation():
    order = OrderBuilder().with_status("preparation").build()

    assert order._status.value == "Preparation"


def test_order_status_value_should_be_ready():
    order = OrderBuilder().with_status("ready").build()

    assert order._status.value == "Ready"


def test_order_status_value_should_be_delivered():
    order = OrderBuilder().with_status("delivered").build()

    assert order._status.value == "Delivered"


def test_order_should_change_from_waiting_to_preparation():
    order = OrderBuilder().with_status("waiting").build()

    order.process()

    assert order._status.value == "Preparation"


def test_order_should_change_from_preparation_to_ready():
    order = OrderBuilder().with_status("preparation").build()

    order.process()

    assert order._status.value == "Ready"


def test_order_should_change_from_ready_to_delivered():
    order = OrderBuilder().with_status("ready").build()

    order.process()

    assert order._status.value == "Delivered"


def test_order_should_not_change_from_delivered():
    order = OrderBuilder().with_status("delivered").build()

    with pytest.raises(Exception) as excinfo:
        order.process()

    assert "Delivered order cannot be processed" in str(excinfo.value)
