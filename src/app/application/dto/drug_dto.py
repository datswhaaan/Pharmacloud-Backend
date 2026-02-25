from dataclasses import dataclass

@dataclass
class DrugImageDTO:
    image_url: str
    view_type: str
    position: int
    lighting: str

@dataclass
class DrugImageListDTO:
    images: list[DrugImageDTO]
    
@dataclass
class DrugDTO:
    b_item_id: str
    item_number: str
    item_common_name: str
    item_active: str
    item_trade_name: str | None = None
    item_nick_name: str | None = None
    b_item_subgroup_id: str | None = None
    b_item_billing_subgroup_id: str | None = None
    b_item_16_group_id: str | None = None
    images: list[DrugImageDTO] = None
    instructions: list[dict] = None

@dataclass
class DrugListDTO:
    drugs: list[DrugDTO]