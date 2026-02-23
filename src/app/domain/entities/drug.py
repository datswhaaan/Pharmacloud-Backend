from dataclasses import dataclass

@dataclass
class DrugImage:
    b_item_image_id: str
    b_item_id: str
    item_image_url: str
    f_image_variant_id: str

@dataclass
class DrugInstruction:
    b_item_drug_id: str
    b_item_id: str
    item_drug_caution: str
    b_item_drug_instruction_id: str
    item_drug_description: str
    item_drug_special_prescription_text: str
    instruction_text: str

@dataclass
class Drug:
    b_item_id: str
    item_number: str
    item_common_name: str
    item_active: str
    item_trade_name: str | None = None
    item_nick_name: str | None = None
    b_item_subgroup_id: str | None = None
    b_item_billing_subgroup_id: str | None = None
    b_item_16_group_id: str | None = None
    images: list[DrugImage] = None
    instructions: list[DrugInstruction] = None

@dataclass
class DrugList:
    drugs: list[Drug]