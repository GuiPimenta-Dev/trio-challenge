from src.application.ports.repositories.orders import OrdersRepository

from . import UseCase


class ViewOrderDetails(UseCase):
    def __init__(self, orders_repository: OrdersRepository) -> None:
        self.orders_repository = orders_repository

    def execute(self):
        orders = self.orders_repository.list_all()
        result = []

        for order in orders:
            products = [
                {
                    "name": product.name,
                    "variation": product.variation,
                }
                for product in order.products
            ]
            result.append(
                {
                    "id": order.id,
                    "customer_id": order.customer_id,
                    "location": order.location,
                    "status": order.status,
                    "products": products,
                }
            )

        return result
