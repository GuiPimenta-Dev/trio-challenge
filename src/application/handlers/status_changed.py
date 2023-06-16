from src.application.handlers import Handler
from src.application.ports.gateways.mailer import Mailer
from src.application.ports.repositories.customers import CustomersRepository
from src.domain.events.status_changed import StatusChanged


class StatusChangedHandler(Handler):
    name = "state_changed"

    def __init__(self, mailer: Mailer, customers_repository: CustomersRepository):
        self.mailer = mailer
        self.customers_repository = customers_repository

    def handle(self, event: StatusChanged) -> None:
        customer = self.customers_repository.find_by_id(event.customer_id)

        self.mailer.send(
            to=customer.email,
            subject="Order status changed",
            body=f"Order status changed to {event.status}",
        )
