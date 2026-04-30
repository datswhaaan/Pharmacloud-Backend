from app.infrastructure.models.detection import DetectionORM, DetectionItemORM
from app.domain.entities.detection import DetectionList, Detection, DetectionItem, DetectionCreate

def _to_detection(orm: DetectionORM) -> Detection:
    return Detection(
            detection_id=orm.detection_id,
            detected_at=orm.detected_at,
            image_url=orm.image_url,
            verified_by=orm.employee.employee_firstname + " " + orm.employee.employee_lastname if orm.employee else "",
            verified_at=orm.verified_at,
            status=orm.status,
            detections=[
                DetectionItem(
                    t_order_drug_id=di.t_order_drug_id,
                    detection_item_id=di.detection_item_id,
                    b_item_id=di.b_item_id,
                    item_common_name=di.item.item_common_name,
                    confidence=di.confidence,
                    quantity=di.quantity,
                    unit=di.item.item_drug[0].item_drug_uom.item_drug_uom_description if di.item.item_drug else "หน่วย",
                    is_manually_edited=di.is_manually_edited,
                    match_type=di.match_type,
                    error_type=di.error_type
                )
                for di in orm.detection_item
            ]
        )

def _to_detection_list(orms: list[DetectionORM]) -> DetectionList:
    return DetectionList(
        detections=[_to_detection(orm) for orm in orms]
    )

def _to_detection_orm(d: DetectionCreate, image_url: str) -> DetectionORM:
    return DetectionORM(
        t_order_id=d.t_order_id,
        status=d.status,
        image_url=image_url
    )

def _to_detection_item_orm(detection_list: list[DetectionItem], detection_id: str) -> list[DetectionItemORM]:
    return [
        DetectionItemORM(
            t_order_drug_id=di.t_order_drug_id,
            detection_id=detection_id,
            b_item_id=di.b_item_id,
            confidence=di.confidence,
            quantity=di.quantity,
            match_type=di.match_type
        ) for di in detection_list
    ]