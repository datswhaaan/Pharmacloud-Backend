from dataclasses import dataclass

@dataclass
class ImageVariant:
    variant_id: int
    view_type: str
    position: int
    lighting: str
    description: str

@dataclass
class ImageVariantList:
    variants: list[ImageVariant]
@dataclass
class DrugImage:
    image_url: str
    view_type: str | None = None
    position: int | None = None
    lighting: str | None = None
    variant_id: int | None = None

@dataclass
class DrugImageList:
    b_item_id: str
    images: list[DrugImage]

@dataclass
class DrugInstruction:
    b_item_drug_id: str
    b_item_id: str
    item_drug_caution: str
    b_item_drug_instruction_id: str
    item_drug_description: str
    item_drug_special_prescription_text: str
    instruction_text: str
    high_alert: bool

@dataclass
class Drug:
    b_item_id: str
    item_number: str
    item_common_name: str
    item_active: str
    item_trade_name: str | None = None
    item_nick_name: str | None = None
    b_item_subgroup: str | None = None
    b_item_billing_subgroup: str | None = None
    b_item_16_group: str | None = None
    images: list[DrugImage] | None = None
    instructions: list[DrugInstruction] = None

@dataclass
class DrugListItem:
    drug_id: str
    drug_code: str
    drug_common_name: str
    high_alert: bool

@dataclass
class DrugList:
    drugs: list[DrugListItem]
    total: int
    page: int
    size: int