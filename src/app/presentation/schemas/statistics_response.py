from pydantic import BaseModel

class DetectionLogItemResponse(BaseModel):
    detection_id: str
    order_id: str
    visit_hn: str
    visit_vn: str
    patient_name: str
    verified_by: str
    verified_at: str

class DetectionLogResponse(BaseModel):
    detections: list[DetectionLogItemResponse]
    total: int
    page: int
    size: int

class SummaryResponse(BaseModel):
    label: list[str]
    value: list[int]

class StatisticsResponse(BaseModel):
    status_summary: SummaryResponse
    error_summary: SummaryResponse
    annual_error_summary: SummaryResponse