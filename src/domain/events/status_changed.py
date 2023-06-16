from dataclasses import dataclass

from . import Event


@dataclass
class StatusChanged(Event):
    name = "state_changed"
    customer_id: str
    status: str
