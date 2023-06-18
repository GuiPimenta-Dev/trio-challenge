from dataclasses import dataclass
from typing import List, Optional

from src.application.errors.bad_request import BadRequest
from src.application.ports.repositories.products import ProductsRepository
from src.domain.entities.product import Product


@dataclass
class ProductDTO:
    name: str
    variation: Optional[str]


class ProductsService:
    def __init__(self, products_repository: ProductsRepository):
        self.products_repository = products_repository

    def get_products(self, products: List[ProductDTO]) -> List[Product]:
        if not products:
            raise BadRequest("There must be at least one product")

        result = []
        for product_dto in products:
            product = self.products_repository.find_by_name(product_dto.get("name"))

            if not product:
                raise BadRequest("Invalid product")

            if product_dto.get("variation"):
                product.choose_variation(product_dto.get("variation"))

            result.append(product)

        return result
