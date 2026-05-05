from PIL import Image, ImageDraw, ImageFont
import io
from app.domain.entities.detection import DetectedMedicationItem, DetectedMedication, DetectionImageInput
from app.infrastructure.mappers.external.medication_vision_inference_mapper import _to_detected_medication
from app.domain.external.medication_vision_inference import MedicationVisionInferenceService

class MedicationVisionInferenceImpl(MedicationVisionInferenceService):
    def __init__(self, model):
        self.model = model

    def infer(self, image: DetectionImageInput) -> DetectedMedication:
        img = Image.open(io.BytesIO(image.content)).convert("RGB")
        width, height = img.size
        draw = ImageDraw.Draw(img)

        result = self.model.predict(image.content)

        detected_items = []

        for det in result["detections"]:
            class_name = det["class_name"]
            confidence = float(det["top1_conf"])
            flag = det["flag"]

            obb_points = [
                (int(p[0] * width), int(p[1] * height))
                for p in det["obb_box"]
            ]

            detected_items.append(
                DetectedMedicationItem(
                    drug_code=class_name,
                    confidence=confidence,
                    flag=flag,
                    obb_box=obb_points, 
                )
            )

            draw.polygon(obb_points, outline="green", width=3)

            xs = [p[0] for p in obb_points]
            ys = [p[1] for p in obb_points]
            text_pos = (min(xs), min(ys) - 20)

            label = f"{class_name} ({confidence:.2f})"

            draw.rectangle(
                [text_pos, (text_pos[0] + 200, text_pos[1] + 20)],
                fill="green"
            )

            draw.text(
                text_pos,
                label,
                fill="white",
                font=ImageFont.truetype("arial.ttf", 24)
            )

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        processed_image = buffer.getvalue()

        return DetectedMedication(
            content=processed_image,
            content_type="image/jpeg",
            detected_items=detected_items,
        )