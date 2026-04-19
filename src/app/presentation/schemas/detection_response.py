from pydantic import BaseModel
from app.presentation.schemas.prescription_response import OrderDrugResponse

class DetectionItemResponse(BaseModel):
    t_order_drug_id: str | None = None
    detection_item_id: str
    item_common_name: str
    confidence: float
    confidence_level: str
    quantity: int | None = None
    unit: str
    is_manually_edited: bool
    match_type: str

class DetectionResponse(BaseModel):
    detection_id: str
    image_url: str
    status: str
    verified_by: str
    verified_at: str
    drug_list: list[DetectionItemResponse]

class DetectionListResponse(BaseModel):
    order_drugs: list[OrderDrugResponse]
    detections: list[DetectionResponse]