from dataclasses import dataclass

@dataclass
class DetectionLogItem:
    detection_id: str
    order_id: str
    visit_hn: str
    visit_vn: str
    patient_prefix: str
    patient_firstname: str
    patient_lastname: str
    employee_firstname: str
    employee_lastname: str
    verified_at: str
    
@dataclass
class DetectionLog:
    detections: list[DetectionLogItem]
    total: int
    page: int
    size: int

@dataclass
class SummaryItem:
    key: str
    label: str
    value: int

@dataclass
class Summary:
    data: list[SummaryItem]