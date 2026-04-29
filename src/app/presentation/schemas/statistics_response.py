from pydantic import BaseModel

class DetectionLogItemResponse(BaseModel):
    detection_id: str
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