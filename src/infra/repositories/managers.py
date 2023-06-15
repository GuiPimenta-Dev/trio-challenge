from src.application.ports.repositories.managers import ManagersRepository
from src.domain.entities.manager import Manager


class InMemoryManagersRepository(ManagersRepository):
    def __init__(self):
        self.managers: Manager = []

    def add(self, manager: Manager):
        self.managers.append(manager)

    def find_by_id(self, id: str) -> Manager:
        return next(
            (manager for manager in self.managers if manager.get("id") == id), None
        )
