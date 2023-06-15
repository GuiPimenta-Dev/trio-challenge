from src.application.usecases import UseCase


class CancelOrder(UseCase):
    def __init__(self, customers_repository, orders_repository):
        self.customers_repository = customers_repository
        self.orders_repository = orders_repository

    def execute(self, order_id, customer_id):
        customer = self.customers_repository.find_by_id(customer_id)
        if not customer:
            raise Exception("Customer not found")

        order = self.orders_repository.find_by_id(order_id)
        if not order:
            raise Exception("Order not found")

        if order.customer_id != customer_id:
            raise Exception("Order does not belong to this customer")

        if order.status != "Waiting":
            raise Exception("Order must be in Waiting status to be canceled")

        self.orders_repository.delete(order_id)
