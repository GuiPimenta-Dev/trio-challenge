from src.application.ports.repositories.orders import OrdersRepository

from . import UseCase


class ViewOrderDetails(UseCase):
    def __init__(self, orders_repository: OrdersRepository) -> None:
        self.orders_repository = orders_repository

    def execute(self):
        return self.orders_repository.list_all()
