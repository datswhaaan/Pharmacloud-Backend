from dataclasses import dataclass

# Used for both input and output
@dataclass
class DrugDTO:
    drug_code: str
    width_mm: float | None = None
    length_mm: float | None = None
    height_mm: float | None = None
    weight_mg: float | None = None
    image_top_path: str | None = None
    image_side_path: str | None = None
    image_front_path: str | None = None
    image_top_path2: str | None = None
    image_side_path2: str | None = None
    image_front_path2: str | None = None

@dataclass
class DrugListDTO:
    drugs: list[DrugDTO]