from dataclasses import dataclass

from src.infra.broker.broker import InMemoryBroker
from src.infra.repositories.customers import InMemoryCustomersRepository
from src.infra.repositories.managers import InMemoryManagersRepository
from src.infra.repositories.orders import InMemoryOrdersRepository
from src.infra.repositories.products import InMemoryProductsRepository
from tests.utils.mocks.mailer_spy import MailerSpy

customers_repository = InMemoryCustomersRepository()
customers_repository.create_default_customer()

managers_repository = InMemoryManagersRepository()
managers_repository.create_default_manager()


@dataclass
class Config:
    customers_repository = customers_repository
    managers_repository = managers_repository
    orders_repository = InMemoryOrdersRepository()
    products_repository = InMemoryProductsRepository()
    broker = InMemoryBroker()
    mailer = MailerSpy()
