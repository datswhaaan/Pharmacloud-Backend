from abc import abstractmethod
from app.domain.entities.prescription import Prescription

class PrescriptionRepository:
    @abstractmethod
    def get_prescription_by_id(self, id: str) -> Prescription | None:
        """Return a prescription by its ID or None if not found"""
        raise NotImplementedError