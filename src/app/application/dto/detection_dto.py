from dataclasses import dataclass
from app.application.dto.prescription_dto import OrderDrugDTO, OrderDrugInferDTO

@dataclass
class DetectionItemDTO:
    t_order_drug_id: str
    detection_item_id: str
    item_common_name: str
    confidence: float
    confidence_level: str
    quantity: str
    unit: str
    is_manually_edited: bool
    match_type: str
    error_type: str | None = None

@dataclass
class DetectionDTO:
    detection_id: str
    image_url: str
    verified_by: str
    verified_at: str
    status: str
    drug_list: list[DetectionItemDTO]


@dataclass
class DetectionInferDTO:
    detection_id: str
    image_url: str
    verified_by: str
    verified_at: str
    status: str
    ordered_drugs: list[OrderDrugInferDTO]
    drug_list: list[DetectionItemDTO]

@dataclass
class DetectionListDTO:
    order_drugs: list[OrderDrugDTO]
    detections: list[DetectionDTO]

@dataclass
class DetectionItemInputDTO:
    b_item_id: str
    confidence: float

@dataclass
class DetectionInputDTO:
    order_id: str
    detections: list[DetectionItemInputDTO]

@dataclass
class DetectionItemUpdateDTO:
    detection_item_id: str
    quantity: int
    is_checked: bool
    error_type: str | None = None

@dataclass
class DetectionUpdateDTO:
    detection_id: str
    status: str
    verified_by: str
    drug_list: list[DetectionItemUpdateDTO]

@dataclass
class DetectionImageInputDTO:
    content: bytes
    content_type: str