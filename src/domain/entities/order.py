from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List

from src.application.errors.bad_request import BadRequest
from src.domain.entities.product import Product


@dataclass
class OrderStatus(ABC):
    @property
    def value(self):
        return self.__class__.__name__.capitalize()

    @abstractmethod
    def process(self, order):  # pragma: no cover
        raise NotImplementedError


class Waiting(OrderStatus):
    def process(self, order):
        order.change_status(Preparation())


class Preparation(OrderStatus):
    def process(self, order):
        order.change_status(Ready())


class Ready(OrderStatus):
    def process(self, order):
        order.change_status(Delivered())


class Delivered(OrderStatus):
    def process(self, order):
        raise BadRequest("Order already delivered")


@dataclass
class Location:
    IN_HOUSE = "in-house"
    TAKE_AWAY = "take-away"


@dataclass
class OrderDTO:
    id: str
    customer_id: str
    products: List[Product]
    location: Location
    status: OrderStatus = Waiting()


class Order:
    def __init__(self, order_dto: OrderDTO):
        self.id = order_dto.id
        self.customer_id = order_dto.customer_id
        self.products = order_dto.products
        self._status = order_dto.status
        self.location = order_dto.location

    @property
    def status(self):
        return self._status.value

    def process(self):
        self._status.process(self)

    def change_status(self, new_status):
        self._status = new_status

    def __repr__(self) -> str:  # pragma: no cover
        return str(
            {
                "id": self.id,
                "customer_id": self.customer_id,
                "products": self.products,
                "status": self._status.value,
            }
        )
