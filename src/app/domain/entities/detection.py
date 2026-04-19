from dataclasses import dataclass
from datetime import datetime

@dataclass
class DetectionItem:
    t_order_drug_id: str
    detection_item_id: str
    b_item_id: str
    item_common_name: str
    confidence: str
    quantity: str
    unit: str
    is_manually_edited: bool
    match_type: str

@dataclass
class Detection:
    detection_id: str
    detected_at: datetime
    status: str
    image_url: str
    verified_by: str
    verified_at: datetime
    detections: list[DetectionItem]

@dataclass
class DetectionList:
    detections: list[Detection]

@dataclass
class DetectionImageInput:
    content: bytes
    content_type: str

@dataclass
class DetectionItemInput:
    t_order_drug_id: str
    b_item_id: str
    confidence: str
    match_type: str
    quantity: str | None = None

@dataclass
class DetectionCreate:
    t_order_id: str
    status: str
    detections: list[DetectionItemInput]