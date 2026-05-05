from abc import ABC, abstractmethod
from app.domain.entities.drug import Drug, DrugImage, DrugImageList, DrugList

class DrugRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Drug | None:
        """Return a drug by its drug id or None if not found"""
        raise 
    
    @abstractmethod
    def get_by_drug_code(self, drug_code: str) -> Drug | None:
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
    
    @abstractmethod
    def add_drug_image(self, drug_id: str, trade_name: str, images: DrugImageList) -> DrugImageList:
        """Add images to a drug"""
        raise NotImplementedError
    
    @abstractmethod
    def delete_drug_image(self, image_ids: list[str]) -> None:
        """Delete drug images"""
        raise NotImplementedError