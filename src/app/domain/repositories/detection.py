from abc import abstractmethod
from app.domain.entities.detection import DetectionList, DetectionImageInput, Detection, DetectionCreate, DetectionUpdate

class DetectionRepository:
    @abstractmethod
    def get_detections_by_order_id(self, order_id: str) -> DetectionList:
        """Return a list of detections for a given order ID"""
        raise NotImplementedError

    @abstractmethod
    def get_detections_by_detection_id(self, detection_id: str) -> DetectionList:
        """Return a list of detections for a given order ID"""
        raise NotImplementedError

    @abstractmethod
    def create_detection(self, detection: DetectionCreate, image: DetectionImageInput) -> Detection:
        """Create and store a detection with its associated image data."""
        raise NotImplementedError

    @abstractmethod
    def update_detection(self, detection: DetectionUpdate) -> Detection:
        """Update the status and verification details of an existing detection."""
        raise NotImplementedError