from abc import abstractmethod
from app.domain.entities.detection import DetectionList, DetectionImageInput, Detection

class DetectionRepository:
    @abstractmethod
    def get_detections_by_order_id(self, order_id: str) -> DetectionList:
        """Return a list of detections for a given order ID"""
        raise 

    @abstractmethod
    def create_detection(self, detection: Detection, image: DetectionImageInput) -> Detection:
        """Create and store a detection with its associated image data."""
        raise