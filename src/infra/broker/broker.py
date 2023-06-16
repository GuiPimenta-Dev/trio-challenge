from typing import List

from src.application.handlers import Handler
from src.application.ports.broker.broker import Broker
from src.domain.events import Event


class InMemoryBroker(Broker):
    handlers: List[Handler] = []

    def publish(self, event: Event) -> None:
        for handler in self.handlers:
            if handler.name == event.name:
                handler.handle(event)

    def subscribe(self, handler: Handler) -> None:
        self.handlers.append(handler)
