from app.domain.repositories.drug import DrugRepository
from app.application.dto.drug_dto import DrugDTO, DrugListDTO
from app.application.mappers.drug_mapper import _to_drug, _to_dto, _to_dto_list

class DrugService:
    def __init__(self, repository: DrugRepository):
        self.repository = repository

    def get_by_id(self, id: str) -> DrugDTO | None:
        drug = self.repository.get_by_id(id)
        if drug is None:
            return None
        return _to_dto(drug)

    def get_all(
        self,
        search: str | None = None,
        *,
        high_alert: bool | None = None,
        skip: int = 0,
        limit: int = 100
    ) -> DrugListDTO:
        drugs = self.repository.get_all(search, high_alert=high_alert, skip=skip, limit=limit)
        return _to_dto_list(drugs)
    
    def update(self, input: DrugDTO) -> DrugDTO:
        drug = _to_drug(input)
        updated = self.repository.update(drug)
        return _to_dto(updated)