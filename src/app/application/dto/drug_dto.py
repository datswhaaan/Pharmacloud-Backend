from dataclasses import dataclass

@dataclass
class DrugImageDTO:
    id: str
    image_url: str
    view_type: str
    position: int
    lighting: str
    created_at: str

@dataclass
class DrugImageInputDTO:
    content: bytes
    content_type: str
    view_type: str | None = None
    position: int | None = None
    lighting: str | None = None

@dataclass
class DrugImageListInputDTO:
    b_item_id: str
    images: list[DrugImageInputDTO]

@dataclass
class DrugImageListDTO:
    images: list[DrugImageDTO]

@dataclass
class DrugNameDTO:
    generic: str
    trade: str
    thai: str

@dataclass
class DrugCategoryDTO:
    therapeutic: str
    pharmacological: str
    standard: str

@dataclass
class DrugFlagsDTO:
    is_high_alert: bool
    has_images: bool

@dataclass
class DrugInstructionDTO:
    caution: str
    description: str
    special_prescription: str
    instruction: str

@dataclass
class DrugDTO:
    id: str
    code: str
    names: DrugNameDTO
    categories: DrugCategoryDTO | None = None
    images: list[DrugImageDTO] | None = None
    instructions: DrugInstructionDTO | None = None

@dataclass
class DrugListItemDTO:
    drug_id: str
    drug_code: str
    drug_common_name: str
    flags: DrugFlagsDTO

@dataclass
class DrugListDTO:
    drugs: list[DrugDTO]
    total: int
    page: int
    size: int