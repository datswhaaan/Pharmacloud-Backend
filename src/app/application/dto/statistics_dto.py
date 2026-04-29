from dataclasses import dataclass

@dataclass
class DetectionLogItemDTO:
    detection_id: str
    visit_hn: str
    visit_vn: str
    patient_name: str
    status: str
    verified_by: str
    verified_at: str

@dataclass
class DetectionLogDTO:
    detections: list[DetectionLogItemDTO]
    total: int
    page: int
    size: int