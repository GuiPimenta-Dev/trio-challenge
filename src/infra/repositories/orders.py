from copy import deepcopy
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

    def find_by_id(self, order_id: int) -> Order:
        for order in self.orders:
            if order.id == order_id:
                return deepcopy(order)

    def update(self, order: Order):
        for index, order_in_list in enumerate(self.orders):
            if order_in_list.id == order.id:
                self.orders[index] = deepcopy(order)
                return

    def delete(self, order_id: str) -> None:
        for index, order in enumerate(self.orders):
            if order.id == order_id:
                del self.orders[index]
                return
