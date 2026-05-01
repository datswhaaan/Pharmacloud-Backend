from dataclasses import dataclass

@dataclass
class DetectionLogItemDTO:
    detection_id: str
    order_id: str
    visit_hn: str
    visit_vn: str
    patient_name: str
    verified_by: str
    verified_at: str

@dataclass
class DetectionLogDTO:
    detections: list[DetectionLogItemDTO]
    total: int
    page: int
    size: int

@dataclass
class SummaryItemDTO:
    key: str
    label: str
    value: int

@dataclass
class SummaryDTO:
    data: list[SummaryItemDTO]

@dataclass
class StatisticsDTO:
    status_summary: SummaryDTO
    error_summary: SummaryDTO
    annual_error_summary: SummaryDTO