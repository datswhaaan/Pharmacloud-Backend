from datetime import datetime, timezone
from app.domain.entities.detection import DetectionList, DetectionItem, Detection, DetectionItemInput, DetectionImageInput, DetectionCreate, DetectionUpdate, DetectionItemUpdate
from app.domain.entities.prescription import OrderList, OrderDrugItem
from app.application.dto.detection_dto import DetectionDTO, DetectionListDTO, DetectionItemDTO, DetectionInferDTO, DetectionUpdateDTO
from app.application.dto.prescription_dto import OrderDrugDTO, OrderDrugInferDTO

def _to_detection_item_compare_dto(
    ordered: OrderDrugItem | None,
    detected: DetectionItem | None,
    match_type: str
) -> DetectionItemDTO:
    return DetectionItemDTO(
        t_order_drug_id=ordered.t_order_drug_id if ordered else "",
        detection_item_id=detected.detection_item_id if detected else "",
        item_common_name=ordered.item_common_name if ordered else detected.item_common_name,
        confidence=detected.confidence if detected else "0",
        confidence_level=_confidence_level_mapper(detected.confidence) if detected else "",
        quantity=detected.quantity if detected else ordered.quantity,
        unit=ordered.unit if ordered else detected.unit,
        is_manually_edited=detected.is_manually_edited if detected else False,
        match_type=match_type
    )

def _to_detection_item_dto(di: DetectionItem) -> DetectionItemDTO:
    return DetectionItemDTO(
        t_order_drug_id=di.t_order_drug_id if di.t_order_drug_id else "",
        detection_item_id=di.detection_item_id,
        item_common_name=di.item_common_name,
        confidence=di.confidence,
        confidence_level=_confidence_level_mapper(di.confidence),
        quantity=di.quantity,
        unit=di.unit,
        is_manually_edited=di.is_manually_edited,
        match_type=di.match_type
    )

def _to_detection_dto(detection: Detection, drug_list: list[DetectionItemDTO]) -> DetectionDTO:
    return DetectionDTO(
        detection_id=detection.detection_id,
        image_url=detection.image_url,
        status=detection.status,
        verified_at=str(detection.verified_at),
        verified_by=detection.verified_by,
        drug_list=[_to_detection_item_dto(drug) for drug in drug_list]
    )

def _to_detection_list_dto(order_list: OrderList, detection_list: DetectionList) -> DetectionListDTO:
    return DetectionListDTO(
        order_drugs=[
            OrderDrugDTO(
                t_order_drug_id=od.t_order_drug_id,
                item_common_name=od.item_common_name,
                unit=od.unit,
                quantity=od.quantity
            ) for od in order_list.orders
        ],
        detections=[_to_detection_dto(d, d.detections) for d in detection_list.detections]
    )

def _to_detection_item_input(
    ordered: OrderDrugItem | None,
    detected: DetectionItem | None,
    match_type: str
) -> DetectionItemInput:
    return DetectionItemInput(
        t_order_drug_id=ordered.t_order_drug_id if ordered else None,
        b_item_id=detected.b_item_id,
        confidence=detected.confidence,
        quantity=ordered.quantity if ordered else None,
        match_type=match_type
    )

def _to_detection(
        order_id: str,
        detection_items: list[DetectionItemInput]
) -> DetectionCreate:
    return DetectionCreate(
        t_order_id=order_id,
        status=4, #รอตรวจสอบ
        detections=detection_items
    )

def _to_detection_image(image: bytes) -> DetectionImageInput:
    content = image.file.read()
    return DetectionImageInput(
        content=content,
        content_type=image.content_type
    )

def _to_detection_update(detection: DetectionUpdateDTO, drug_list: list[DetectionItemUpdate], is_edited: bool) -> DetectionUpdate:
    return DetectionUpdate(
        detection_id=detection.detection_id,
        status=_status_text_to_id(detection.status) if not is_edited else 3,
        verified_by=detection.verified_by,
        verified_at=datetime.now(timezone.utc),
        drug_list=_to_detection_item_update_list(drug_list)
    )

def _to_detection_item_update_list(detection_items: list[DetectionItem]) -> list[DetectionItemUpdate]:
    return [
        DetectionItemUpdate(
            detection_item_id=item.detection_item_id,
            quantity=item.quantity,
            is_manually_edited=item.is_manually_edited,
            match_type=item.match_type
        ) for item in detection_items
    ]

def _to_infer_detection_dto(detection: Detection, detected_drug_list: list[DetectionItemDTO], ordered_drug_list: list[OrderDrugInferDTO]) -> DetectionInferDTO:
    return DetectionInferDTO(
        detection_id=detection.detection_id,
        image_url=detection.image_url,
        status=detection.status,
        verified_at=str(detection.verified_at),
        verified_by=detection.verified_by,
        ordered_drugs=ordered_drug_list,
        drug_list=detected_drug_list
    )

def _confidence_level_mapper(confidence_level: float) -> str:
    if confidence_level >= 0.80:
        return "High"
    elif confidence_level >=0.60:
        return "Medium"
    else: return "Low"

STATUS_MAP = {
    1: "approved",
    2: "rejected",
    3: "edited",
    4: "waited"
}

def _status_id_to_text(status_id: int) -> str:
    return STATUS_MAP.get(status_id, "ไม่ทราบสถานะ")

def _status_text_to_id(status_text: str) -> int | None:
    reverse_map = {v: k for k, v in STATUS_MAP.items()}
    return reverse_map.get(status_text)