from pydantic import BaseModel

class DrugImageSchema(BaseModel):
    b_item_image_id: str
    b_item_id: str
    image_url: str
    variant: dict | None = None

class DrugInstructionSchema(BaseModel):
    b_item_drug_id: str
    b_item_id: str
    item_drug_caution: str
    b_item_drug_instruction_id: str
    item_drug_description: str
    item_drug_special_prescription_text: str
    instruction_text: str
    high_alert: bool
class DrugSchema(BaseModel):
    b_item_id: str
    item_number: str
    item_common_name: str
    item_active: str
    item_trade_name: str | None = None
    item_nick_name: str | None = None
    b_item_subgroup_id: str | None = None
    b_item_billing_subgroup_id: str | None = None
    b_item_16_group_id: str | None = None
    images: list[DrugImageSchema] = None
    instructions: list[DrugInstructionSchema] = None

class DrugUpdateSchema(BaseModel):
    item_number: str | None = None
    item_common_name: str | None = None
    item_trade_name: str | None = None
    item_nick_name: str | None = None
    b_item_subgroup_id: str | None = None
    b_item_billing_subgroup_id: str | None = None
    b_item_16_group_id: str | None = None
    b_specimen_id: str | None = None

class DrugListSchema(BaseModel):
    drugs: list[DrugSchema]