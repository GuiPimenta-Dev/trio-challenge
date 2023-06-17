import os
from dataclasses import dataclass

from dotenv import load_dotenv

from src.application.handlers.status_changed import StatusChangedHandler
from src.domain.entities.customer import Customer
from src.domain.entities.manager import Manager
from src.infra.broker.broker import InMemoryBroker
from src.infra.gateways.smtp_adapter import SmtpAdapter
from src.infra.repositories.customers import InMemoryCustomersRepository
from src.infra.repositories.managers import InMemoryManagersRepository
from src.infra.repositories.orders import InMemoryOrdersRepository
from src.infra.repositories.products import InMemoryProductsRepository

load_dotenv()

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

customers_repository = InMemoryCustomersRepository()
customer = Customer(id="customer", email=username)
customers_repository.add(customer)

managers_repository = InMemoryManagersRepository()
manager = Manager(id="manager")
managers_repository.add(manager)

mailer = SmtpAdapter(username, password)

broker = InMemoryBroker()
status_changed_handler = StatusChangedHandler(mailer, customers_repository)
broker.subscribe(status_changed_handler)


@dataclass
class Config:
    customers_repository = customers_repository
    managers_repository = managers_repository
    orders_repository = InMemoryOrdersRepository()
    products_repository = InMemoryProductsRepository()
    broker = broker
