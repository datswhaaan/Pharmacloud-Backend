from pydantic import BaseModel

class DetectionItemCreateRequest(BaseModel):
    b_item_id: str
    confidence: float

class DetectionCreateRequest(BaseModel):
    drug_list: list[DetectionItemCreateRequest]