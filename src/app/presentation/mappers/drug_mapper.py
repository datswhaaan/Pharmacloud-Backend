from app.presentation.schemas.drug import DrugSchema
from app.application.dto.drug_dto import DrugDTO

def _schema_to_drug_dto(input: DrugSchema) -> DrugDTO:
    return DrugDTO(**input.model_dump())

def _base_to_drug_dto(id: str, input: DrugSchema) -> DrugDTO:

    data = input.model_dump()
    
    return DrugDTO(
        b_item_id=id,
        **data 
    )