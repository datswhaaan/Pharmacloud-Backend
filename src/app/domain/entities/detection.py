from dataclasses import dataclass
from datetime import datetime

@dataclass
class DetectionItem:
    detection_item_id: str
    b_item_id: str
    item_common_name: str
    confidence: str
    quantity: str
    unit: str
    is_manually_edited: bool

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