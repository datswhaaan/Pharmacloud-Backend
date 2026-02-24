from abc import ABC, abstractmethod
from app.domain.entities.drug import Drug, DrugList

class DrugRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Drug | None:
        """Return a drug by its drug code or None if not found"""
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        search: str | None = None,
        *,
        high_alert: bool | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> DrugList:
        """Return list of drugs"""
        raise NotImplementedError