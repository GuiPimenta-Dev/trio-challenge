from dataclasses import dataclass
from typing import List, Optional

from src.application.errors.bad_request import BadRequest
from src.application.errors.not_found import NotFound
from src.application.errors.unauthorized import Unauthorized
from src.application.ports.repositories.customers import CustomersRepository
from src.application.ports.repositories.orders import OrdersRepository
from src.application.ports.repositories.products import ProductsRepository
from src.application.usecases import UseCase
from src.domain.entities.order import Location, Order, OrderDTO
from src.domain.service.products import ProductsService


@dataclass
class Repositories:
    customer_repository: CustomersRepository
    products_repository: ProductsRepository
    orders_repository: OrdersRepository


@dataclass
class ProductDTO:
    name: str
    variation: Optional[str]


@dataclass
class InputDTO:
    order_id: str
    customer_id: str
    products: List[ProductDTO]
    location: Location


class UpdateOrder(UseCase):
    def __init__(self, repositories: Repositories) -> None:
        self.customer_repository = repositories["customers_repository"]
        self.orders_repository = repositories["orders_repository"]
        self.products_repository = repositories["products_repository"]

    def execute(self, new_order: InputDTO):
        customer = self.customer_repository.find_by_id(new_order.get("customer_id"))
        if not customer:
            raise NotFound("Customer not found")

        old_order = self.orders_repository.find_by_id(new_order.get("order_id"))
        if not old_order:
            raise NotFound("Order not found")

        if old_order.customer_id != customer.id:
            raise Unauthorized("Customer not allowed to update this order")

        if old_order.status != "Waiting":
            raise BadRequest(
                "Order cannot be updated with a status different than Waiting"
            )

        location = new_order.get("location", old_order.location)
        if location not in [Location.IN_HOUSE, Location.TAKE_AWAY]:
            raise BadRequest("Invalid location")

        products_service = ProductsService(self.products_repository)
        products = products_service.get_products(new_order.get("products"))

        order_dto = OrderDTO(
            id=old_order.id,
            customer_id=old_order.customer_id,
            products=products,
            location=location,
        )
        updated_order = Order(order_dto)
        self.orders_repository.update(updated_order)
