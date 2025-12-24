from app.presentation.schemas.drug import DrugBase, DrugSchema
from app.application.dto.drug_dto import DrugDTO

def _schema_to_drug_dto(input: DrugSchema) -> DrugDTO:
    return DrugDTO(**input.model_dump())

def _base_to_drug_dto(drug_code: str, input: DrugBase) -> DrugDTO:

    data = input.model_dump()
    
    return DrugDTO(
        drug_code=drug_code,
        **data 
    )