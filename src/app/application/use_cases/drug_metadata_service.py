from app.domain.repositories.drug_metadata import DrugMetadataRepository
from app.application.dto.drug_metadata_dto import DrugMetadataDTO, DrugMetadataListDTO
from app.application.mappers.drug_metadata_mapper import _to_drug, _to_dto, _to_dto_list

class DrugMetadataService:
    def __init__(self, repository: DrugMetadataRepository):
        self.repository = repository

    def create(self, input: DrugMetadataDTO) -> DrugMetadataDTO:
        drug = _to_drug(input)
        saved = self.repository.create(drug)
        return _to_dto(saved)

    def get_by_drug_code(self, drug_code: str) -> DrugMetadataDTO | None:
        drug = self.repository.get_by_drug_code(drug_code)
        if drug is None:
            return None
        return _to_dto(drug)

    def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> DrugMetadataListDTO:
        drugs = self.repository.get_all(skip=skip, limit=limit)
        return _to_dto_list(drugs)
    
    def update(self, input: DrugMetadataDTO) -> DrugMetadataDTO:
        drug = _to_drug(input)
        updated = self.repository.update(drug)
        return _to_dto(updated)
    
    def delete(self, drug_code: str) -> None:
        self.repository.delete(drug_code)
