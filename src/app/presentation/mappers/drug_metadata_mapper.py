from app.presentation.schemas.drug_metadata import DrugMetadataBase, DrugMetadataSchema
from app.application.dto.drug_metadata_dto import DrugMetadataDTO

def _schema_to_drug_dto(input: DrugMetadataSchema) -> DrugMetadataDTO:
    return DrugMetadataDTO(**input.model_dump())

def _base_to_drug_dto(drug_code: str, input: DrugMetadataBase) -> DrugMetadataDTO:

    data = input.model_dump()
    
    return DrugMetadataDTO(
        drug_code=drug_code,
        **data 
    )