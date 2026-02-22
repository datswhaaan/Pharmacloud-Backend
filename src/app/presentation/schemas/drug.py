from pydantic import BaseModel

class DrugSchema(BaseModel):
    b_item_id: str
    item_number: str
    item_common_name: str
    item_active: str
    item_trade_name: str | None = None
    item_nick_name: str | None = None
    b_item_subgroup_id: str | None = None
    b_item_billing_subgroup_id: str | None = None
    item_printable: str | None = None
    item_secret: str | None = None
    b_item_16_group_id: str | None = None
    f_item_lab_type_id: str | None = None
    b_specimen_id: str | None = None

class DrugUpdateSchema(BaseModel):
    item_number: str | None = None
    item_common_name: str | None = None
    item_trade_name: str | None = None
    item_nick_name: str | None = None
    item_active: str | None = None
    b_item_subgroup_id: str | None = None
    b_item_billing_subgroup_id: str | None = None
    item_printable: str | None = None
    item_secret: str | None = None
    b_item_16_group_id: str | None = None
    f_item_lab_type_id: str | None = None
    b_specimen_id: str | None = None

class DrugListSchema(BaseModel):
    drugs: list[DrugSchema]