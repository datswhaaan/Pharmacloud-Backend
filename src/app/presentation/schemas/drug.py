from pydantic import BaseModel

class DrugImageDTO(BaseModel):
    image_url: str
    view_type: str | None = None
    position: int | None = None
    lighting: str | None = None

class DrugImageListDTO(BaseModel):
    images: list[DrugImageDTO]

class DrugInstructionDTO(BaseModel):
    b_item_drug_id: str
    b_item_id: str
    item_drug_caution: str
    b_item_drug_instruction_id: str
    item_drug_description: str
    item_drug_special_prescription_text: str
    instruction_text: str
    high_alert: bool
    
class DrugDTO(BaseModel):
    b_item_id: str
    item_number: str
    item_common_name: str
    item_active: str
    item_trade_name: str | None = None
    item_nick_name: str | None = None
    b_item_subgroup_id: str | None = None
    b_item_billing_subgroup_id: str | None = None
    b_item_16_group_id: str | None = None
    images: list[DrugImageDTO] | None = None
    instructions: list[DrugInstructionDTO] = None
    
class DrugListDTO(BaseModel):
    drugs: list[DrugDTO]