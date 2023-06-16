from src.application.usecases import UseCase


class CancelOrder(UseCase):
    def __init__(self, orders_repository):
        self.orders_repository = orders_repository

    def execute(self, order_id):
        order = self.orders_repository.find_by_id(order_id)
        if not order:
            raise Exception("Order not found")

        if order.status != "Waiting":
            raise Exception("Order must be in Waiting status to be canceled")

        self.orders_repository.delete(order_id)
