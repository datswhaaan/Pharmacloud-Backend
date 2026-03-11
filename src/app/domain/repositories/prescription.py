from abc import abstractmethod
from app.domain.entities.prescription import Prescription, PrescriptionList

class PrescriptionRepository:
    @abstractmethod
    def get_prescription_by_id(self, id: str) -> Prescription | None:
        """Return a prescription by its ID or None if not found"""
        raise NotImplementedError
    
    @abstractmethod
    def get_all_prescriptions(self, start_time: str, end_time: str, limit: int, skip: int, order: str) -> PrescriptionList:
        """Return a list of prescriptions within the specified time range with pagination"""
        raise NotImplementedError