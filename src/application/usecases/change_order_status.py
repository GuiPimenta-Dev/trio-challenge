from dataclasses import dataclass

from src.application.ports.gateways.mailer import Mailer
from src.application.ports.repositories.managers import ManagersRepository
from src.application.ports.repositories.orders import OrdersRepository

from . import UseCase


@dataclass
class InputDTO:
    manager_id: int
    order_id: int


class ChangeOrderStatus(UseCase):
    def __init__(
        self,
        managers_repository: ManagersRepository,
        orders_repository: OrdersRepository,
        mailer: Mailer,
    ):
        self.managers_repository = managers_repository
        self.orders_repository = orders_repository
        self.mailer = mailer

    def execute(self, input_dto: InputDTO) -> None:
        manager = self.managers_repository.find_by_id(input_dto.get("manager_id"))
        if not manager:
            raise Exception("You must be a manager to perform this action")

        order = self.orders_repository.find_by_id(input_dto.get("order_id"))
        if not order:
            raise Exception("Order not found")

        order.process()

        self.orders_repository.update(order)

        self.mailer.send(
            to="placeholder-id",
            subject="Order status changed",
            body=f"Order status changed to {order.status}",
        )
