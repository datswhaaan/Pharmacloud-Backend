from abc import abstractmethod
from app.domain.entities.detection import DetectedMedication, DetectionImageInput

class MedicationVisionInferenceService:
    @abstractmethod
    def infer(self, image: DetectionImageInput) -> DetectedMedication:
        """Perform medication detection inference on the provided image and return a list of detected medication items."""
        raise NotImplementedError