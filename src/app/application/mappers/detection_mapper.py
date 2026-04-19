from app.domain.entities.detection import DetectionItem, Detection, DetectionItemInput, DetectionImageInput, DetectionCreate
from app.domain.entities.prescription import OrderList, OrderDrugItem
from app.application.dto.detection_dto import DetectionDTO, DetectionListDTO, DetectionItemDTO, DetectionImageInputDTO, DetectionInputDTO
from app.application.dto.prescription_dto import OrderDrugDTO

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
        t_order_drug_id=di.t_order_drug_id,
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

def _to_detection_list_dto(order_list: OrderList, detection_list: list[DetectionItemDTO]) -> DetectionListDTO:
    return DetectionListDTO(
        order_drugs=[
            OrderDrugDTO(
                t_order_drug_id=od.t_order_drug_id,
                item_common_name=od.item_common_name,
                unit=od.unit,
                quantity=od.quantity
            ) for od in order_list.orders
        ],
        detections=detection_list
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
        detection: DetectionInputDTO,
        detection_items: list[DetectionItemInput]
) -> DetectionCreate:
    return DetectionCreate(
        t_order_id=detection.order_id,
        status=4, #รอตรวจสอบ
        detections=detection_items
    )

def _to_detection_image(image: DetectionImageInputDTO) -> DetectionImageInput:
    return DetectionImageInput(
        content=image.content,
        content_type=image.content_type
    )

def _confidence_level_mapper(confidence_level: float) -> str:
    if confidence_level >= 80:
        return "High"
    elif confidence_level >=60:
        return "Medium"
    else: return "Low"