from src.application.usecases.view_order_details import ViewOrderDetails
from src.domain.entities.product import Product
from src.infra.repositories.orders import InMemoryOrdersRepository
from tests.utils.builders.orders import OrderBuilder


def test_it_should_list_all_orders_details():
    orders_repository = InMemoryOrdersRepository()
    order = OrderBuilder().build()
    orders_repository.add(order)

    view_orders_details = ViewOrderDetails(orders_repository)
    orders = view_orders_details.execute()

    assert len(orders) == 1
