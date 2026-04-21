from pydantic import BaseModel

class DetectionItemCreateRequest(BaseModel):
    b_item_id: str
    confidence: float

class DetectionCreateRequest(BaseModel):
    drug_list: list[DetectionItemCreateRequest]

class DetectionItemUpdateRequest(BaseModel):
    detection_item_id: str
    quantity: int
    is_checked: bool
class DetectionUpdateRequest(BaseModel):
    status: str
    verified_by: str
    drug_list: list[DetectionItemUpdateRequest]