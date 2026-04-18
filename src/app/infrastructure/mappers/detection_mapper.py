from app.infrastructure.models.detection import DetectionORM
from app.domain.entities.detection import DetectionList, Detection, DetectionItem

def _to_detection_list(orms: list[DetectionORM]) -> DetectionList:
    return DetectionList(
        detections=[
            Detection(
                detection_id=orm.detection_id,
                detected_at=orm.detected_at,
                image_url=orm.image_url,
                verified_by=orm.employee.employee_firstname + " " + orm.employee.employee_lastname,
                verified_at=orm.verified_at,
                status=orm.detection_status.detection_status_description,
                detections=[
                    DetectionItem(
                        detection_item_id=di.detection_item_id,
                        b_item_id=di.b_item_id,
                        item_common_name=di.item.item_common_name,
                        confidence=di.confidence,
                        quantity=di.quantity,
                        unit=di.item.item_drug[0].item_drug_uom.item_drug_uom_description if di.item.item_drug else "หน่วย",
                        is_manually_edited=di.is_manually_edited
                    )
                    for di in orm.detection_item
                ]
            ) for orm in orms
        ]
    )
