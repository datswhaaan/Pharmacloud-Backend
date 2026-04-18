from abc import abstractmethod
from app.domain.entities.detection import DetectionList

class DetectionRepository:
    @abstractmethod
    def get_detections_by_order_id(self, order_id: str) -> DetectionList:
        """Return a list of detections for a given order ID"""
        raise NotImplementedError