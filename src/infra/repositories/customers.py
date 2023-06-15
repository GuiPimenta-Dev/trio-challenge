from src.application.ports.repositories.customers import CustomersRepository
from src.domain.entities.customer import Customer


class InMemoryCustomersRepository(CustomersRepository):
    def __init__(self):
        self.customers: Customer = []

    def add(self, customer: Customer):
        self.customers.append(customer)

    def find_by_id(self, id: str) -> Customer:
        return next(
            (customer for customer in self.customers if customer.id == id), None
        )
