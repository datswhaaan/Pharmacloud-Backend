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

class SummaryItemResponse(BaseModel):
    key: str
    label: str
    value: int

class SummaryResponse(BaseModel):
    data: list[SummaryItemResponse]

class StatisticsResponse(BaseModel):
    status_summary: SummaryResponse
    error_summary: SummaryResponse
    annual_error_summary: SummaryResponse