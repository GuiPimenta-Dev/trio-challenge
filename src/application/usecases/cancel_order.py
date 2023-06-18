from src.application.errors.bad_request import BadRequest
from src.application.errors.not_found import NotFound
from src.application.usecases import UseCase


class CancelOrder(UseCase):
    def __init__(self, orders_repository):
        self.orders_repository = orders_repository

    def execute(self, order_id):
        order = self.orders_repository.find_by_id(order_id)
        if not order:
            raise NotFound("Order not found")

        if order.status != "Waiting":
            raise BadRequest("Order must be in Waiting status to be canceled")

        self.orders_repository.delete(order_id)
