from PIL import Image, ImageDraw
import io
from app.domain.entities.detection import DetectedMedicationItem, DetectedMedication, DetectionImageInput
from app.infrastructure.mappers.external.medication_vision_inference_mapper import _to_detected_medication
from app.domain.external.medication_vision_inference import MedicationVisionInferenceService

class MedicationVisionInferenceImpl(MedicationVisionInferenceService):
    def __init__(self, model):
        self.model = model

    def infer(self, image: DetectionImageInput) -> DetectedMedication:
        img = Image.open(io.BytesIO(image.content)).convert("RGB")
        draw = ImageDraw.Draw(img)

        detected_items = [
            DetectedMedicationItem(
                b_item_id="ITM010",
                confidence=0.95,
                bbox=(10, 20, 100, 200)
            ),
            DetectedMedicationItem(
                b_item_id="ITM005",
                confidence=0.95,
                bbox=(120, 50, 200, 180)
            )
        ]

        for item in detected_items:
            draw.rectangle(item.bbox, outline="red", width=3)

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        processed_image = buffer.getvalue()

        return DetectedMedication(
            content=processed_image, 
            content_type=Image.MIME[img.format] if img.format in Image.MIME else "image/jpeg",
            detected_items=detected_items
        )