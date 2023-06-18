import uuid
from dataclasses import dataclass
from typing import List, Optional

from src.application.errors.bad_request import BadRequest
from src.application.errors.not_found import NotFound
from src.application.ports.repositories.customers import CustomersRepository
from src.application.ports.repositories.orders import OrdersRepository
from src.application.ports.repositories.products import ProductsRepository
from src.domain.entities.order import Location, Order, OrderDTO
from src.domain.service.products import ProductsService

from . import UseCase


@dataclass
class ProductDTO:
    name: str
    variation: Optional[str]


@dataclass
class PlaceOrderDTO:
    customer_id: str
    products: List[ProductDTO]
    location: Location


@dataclass
class Repositories:
    customer_repository: CustomersRepository
    products_repository: ProductsRepository
    orders_repository: OrdersRepository


class PlaceOrder(UseCase):
    def __init__(self, repositories: Repositories):
        self.customers_repository = repositories["customers_repository"]
        self.products_repository = repositories["products_repository"]
        self.orders_repository = repositories["orders_repository"]

    def execute(self, order: PlaceOrderDTO) -> None:
        customer = self.customers_repository.find_by_id(order.get("customer_id"))
        if not customer:
            raise NotFound("Customer not found")

        location = order.get("location", Location.IN_HOUSE)
        if location not in [Location.IN_HOUSE, Location.TAKE_AWAY]:
            raise BadRequest("Invalid location")

        products_service = ProductsService(self.products_repository)
        products = products_service.get_products(order.get("products"))

        order_dto = OrderDTO(
            id=str(uuid.uuid4()),
            customer_id=customer.id,
            products=products,
            location=location,
        )
        order = Order(order_dto)
        self.orders_repository.add(order)
