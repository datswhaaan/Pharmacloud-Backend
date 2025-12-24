from app.domain.repositories.drug import DrugRepository
from app.application.dto.drug_dto import DrugDTO, DrugListDTO
from app.application.mappers.drug_mapper import _to_drug, _to_dto, _to_dto_list

class DrugService:
    def __init__(self, repository: DrugRepository):
        self.repository = repository

    def create(self, input: DrugDTO) -> DrugDTO:
        drug = _to_drug(input)
        saved = self.repository.create(drug)
        return _to_dto(saved)

    def get_by_drug_code(self, drug_code: str) -> DrugDTO | None:
        drug = self.repository.get_by_drug_code(drug_code)
        if drug is None:
            return None
        return _to_dto(drug)

    def get_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> DrugListDTO:
        drugs = self.repository.get_all(skip=skip, limit=limit)
        return _to_dto_list(drugs)
    
    def update(self, input: DrugDTO) -> DrugDTO:
        drug = _to_drug(input)
        updated = self.repository.update(drug)
        return _to_dto(updated)
    
    def delete(self, drug_code: str) -> None:
        self.repository.delete(drug_code)
