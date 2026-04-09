from abc import abstractmethod
from app.domain.entities.prescription import DetectionList, OrderList, Prescription, PrescriptionList

class PrescriptionRepository:
    @abstractmethod
    def get_prescription_by_id(self, id: str) -> Prescription | None:
        """Return a prescription by its ID or None if not found"""
        raise NotImplementedError
    
    @abstractmethod
    def get_all_prescriptions(
        self, 
        start_time: str, end_time: str, 
        limit: int, skip: int, order: str, 
        search: str | None = None
    ) -> PrescriptionList:
        """Return a list of prescriptions within the specified time range with pagination"""
        raise NotImplementedError

    @abstractmethod
    def get_detections_by_order_id(self, order_id: str) -> DetectionList:
        """Return a list of detections for a given order ID"""
        raise NotImplementedError
    
    @abstractmethod
    def get_orders_by_order_id(self, order_id: str) -> OrderList:
        """Return a list of orders for a given order ID"""
        raise NotImplementedError
