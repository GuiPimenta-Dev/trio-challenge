from typing import List

from src.application.ports.repositories.orders import OrdersRepository
from src.domain.entities.order import Order


class InMemoryOrdersRepository(OrdersRepository):
    def __init__(self):
        self.orders: Order = []

    def add(self, order: Order):
        self.orders.append(order)

    def list_all(self) -> List[Order]:
        return self.orders
