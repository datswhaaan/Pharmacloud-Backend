
from pydantic import BaseModel, ConfigDict

class DrugImageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    image_url: str
    view_type: str | None = None
    position: int | None = None
    lighting: str | None = None

class DrugInstructionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    b_item_drug_id: str
    b_item_id: str
    item_drug_caution: str
    b_item_drug_instruction_id: str
    item_drug_description: str
    item_drug_special_prescription_text: str
    instruction_text: str
    high_alert: bool

class DrugResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    b_item_id: str
    item_number: str
    item_common_name: str
    item_active: str
    item_trade_name: str | None = None
    item_nick_name: str | None = None
    b_item_subgroup: str | None = None
    b_item_billing_subgroup: str | None = None
    b_item_16_group: str | None = None
    images: list[DrugImageResponse] | None = None
    instructions: list[DrugInstructionResponse] | None = None

class DrugListItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_number: str
    item_common_name: str
    high_alert: bool

class DrugListResponse(BaseModel):
    drugs: list[DrugListItemResponse]
    total: int
    page: int
    size: int
