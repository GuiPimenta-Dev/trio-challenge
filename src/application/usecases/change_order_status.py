from dataclasses import dataclass

from src.application.errors.forbidden import Forbidden
from src.application.errors.not_found import NotFound
from src.application.ports.broker.broker import Broker
from src.application.ports.gateways.mailer import Mailer
from src.application.ports.repositories.managers import ManagersRepository
from src.application.ports.repositories.orders import OrdersRepository
from src.domain.events.status_changed import StatusChanged

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
        broker: Broker,
    ):
        self.managers_repository = managers_repository
        self.orders_repository = orders_repository
        self.broker = broker

    def execute(self, input_dto: InputDTO) -> None:
        manager = self.managers_repository.find_by_id(input_dto.get("manager_id"))
        if not manager:
            raise Forbidden("You must be a manager to perform this action")

        order = self.orders_repository.find_by_id(input_dto.get("order_id"))
        if not order:
            raise NotFound("Order not found")

        order.process()

        self.orders_repository.update(order)

        event = StatusChanged(order.customer_id, order.status)
        self.broker.publish(event)
