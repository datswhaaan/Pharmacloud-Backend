from abc import ABC, abstractmethod
from app.domain.entities.drug_metadata import DrugMetadata, DrugMetadataList

class DrugMetadataRepository(ABC):

    @abstractmethod
    def get_by_drug_code(self, drug_code: int) -> DrugMetadata | None:
        """Return a drug by its drug code or None if not found"""
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> DrugMetadataList:
        """Return list of drugs"""
        raise NotImplementedError

    @abstractmethod
    def create(self, drug: DrugMetadata) -> DrugMetadata:
        """Persist and return created drug"""
        raise NotImplementedError

    @abstractmethod
    def update(self, drug: DrugMetadata) -> DrugMetadata:
        """Update and return drug"""
        raise NotImplementedError

    @abstractmethod
    def delete(self, drug_code: int) -> None:
        """Delete drug by ID"""
        raise NotImplementedError
