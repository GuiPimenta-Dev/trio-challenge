import uuid

from src.domain.entities.order import (
    Delivered,
    Order,
    OrderDTO,
    Preparation,
    Ready,
    Waiting,
)


class OrderBuilder:
    def __init__(self, **kwargs):
        self.products = []
        self.status = "waiting"
        self.customer_id = "default"
        self.states = {
            "waiting": Waiting(),
            "preparation": Preparation(),
            "ready": Ready(),
            "delivered": Delivered(),
        }

    def with_product(self, product):
        self.products.append(product)
        return self

    def with_status(self, status):
        self.status = status
        return self

    def with_customer_id(self, customer_id):
        self.customer_id = customer_id
        return self

    def build(self) -> Order:
        order_dto = OrderDTO(
            id=str(uuid.uuid4()),
            customer_id=self.customer_id,
            products=self.products,
            location="in-house",
        )
        order = Order(order_dto)
        order.change_status(self.states[self.status])
        return order
