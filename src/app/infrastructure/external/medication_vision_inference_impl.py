from app.domain.entities.detection import DetectedMedicationItem, DetectedMedication
from app.infrastructure.mappers.external.medication_vision_inference_mapper import _to_detected_medication
from app.domain.external.medication_vision_inference import MedicationVisionInferenceService

class MedicationVisionInferenceImpl(MedicationVisionInferenceService):
    def __init__(self, model):
        self.model = model

    def infer(self, image: bytes) -> DetectedMedication:
        # raw_predictions = self.model.predict(image)

        # return _to_detected_medication(raw_predictions)
        return DetectedMedication(
            image=image,
            detected_items=[
                DetectedMedicationItem(
                    b_item_id="ITM010",
                    confidence=0.95,
                    bbox=(10, 20, 100, 200)
                )
            ]
        )