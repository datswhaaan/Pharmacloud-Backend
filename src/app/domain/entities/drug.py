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
    id: str
    image_url: str
    created_at: str
    view_type: str | None = None
    position: int | None = None
    lighting: str | None = None

@dataclass
class DrugImageUpload:
    content: bytes
    content_type: str
    variant_id: int | None = None 
    view_type: str | None = None
    position: int | None = None
    lighting: str | None = None

@dataclass
class DrugImageListUpload:
    b_item_id: str
    images: list[DrugImageUpload]

@dataclass
class DrugImageList:
    b_item_id: str
    images: list[DrugImage]

@dataclass
class DrugInstruction:
    item_drug_caution: str
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
    instructions: DrugInstruction | None = None

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