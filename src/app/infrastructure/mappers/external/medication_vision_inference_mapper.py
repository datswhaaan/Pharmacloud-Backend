from app.domain.entities.detection import DetectedMedication, DetectedMedicationItem

def _to_detected_medication(prediction) -> DetectedMedication:
    return DetectedMedication(
        image=prediction.image,
        detected_items=_to_detected_medication_items(prediction.detected_items)
    )

def _to_detected_medication_items(preds) -> list[DetectedMedicationItem]:
        return [
            DetectedMedicationItem(
                b_item_id=p.b_item_id,
                confidence=p.confidence,
                bbox=p.bbox
            )
            for p in preds
        ]