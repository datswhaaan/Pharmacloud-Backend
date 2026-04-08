
import uuid
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class DrugImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    url: str
    view_type: str | None = None
    position: int | None = None
    lighting: str | None = None
    created_at: datetime | None = None

class DrugImageListResponse(BaseModel):
    images: list[DrugImageResponse]

class DrugInstructionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    caution: str
    description: str
    special_prescription: str
    instruction: str

class DrugNameResponse(BaseModel):
    generic: str
    trade: str | None = None
    thai: str | None = None

class DrugCategoryResponse(BaseModel):
    therapeutic: str
    pharmacological: str
    standard: str

class DrugFlagsResponse(BaseModel):
    is_high_alert: bool
    has_images: bool

class DrugResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    code: str
    names: DrugNameResponse
    categories: DrugCategoryResponse
    images: list[DrugImageResponse] | None = None
    instructions: DrugInstructionResponse | None = None

class DrugListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    drug_id: str
    drug_code: str
    drug_common_name: str
    flags: DrugFlagsResponse

class DrugListResponse(BaseModel):
    drugs: list[DrugListItemResponse]
    total: int
    page: int
    size: int
