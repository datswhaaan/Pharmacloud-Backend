from pydantic import BaseModel

class DrugBase(BaseModel):
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

    class Config:
        from_attributes = True

class DrugSchema(DrugBase):
    drug_code: str

class DrugListSchema(BaseModel):
    drugs: list[DrugSchema]

