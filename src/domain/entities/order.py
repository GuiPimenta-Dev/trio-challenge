from dataclasses import dataclass
from enum import Enum
from typing import List

from src.domain.entities.product import Product


@dataclass
class OrderStatus(Enum):
    WAITING = "waiting"
    PREPARATION = "preparation"
    READY = "ready"
    DELIVERED = "delivered"


@dataclass
class OrderDTO:
    id: str
    customer_id: str
    products: List[Product]
    status: OrderStatus = OrderStatus.WAITING


class Order:
    def __init__(self, order_dto: OrderDTO):
        self.id = order_dto.id
        self.customer_id = order_dto.customer_id
        self.products = order_dto.products
        self.status = order_dto.status

    def __repr__(self) -> str:  # pragma: no cover
        return str(
            {
                "id": self.id,
                "customer_id": self.customer_id,
                "products": self.products,
                "status": self.status.value,
            }
        )
